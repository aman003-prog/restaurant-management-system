from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.orders.models import Order
from apps.core.permissions import IsDeliveryCrew, IsManager

from .models import DeliveryAssignment, DeliveryPartner
from .serializers import DeliveryAssignmentSerializer, DeliveryPartnerSerializer

# Create your views here.
class DeliveryPartnerProfileView(generics.RetrieveUpdateAPIView):
    """Allows a delivery partner to view/update their status (e.g., AVAILABLE/OFFLINE)."""

    serializer_class = DeliveryPartnerSerializer
    permission_classes = [IsAuthenticated, IsDeliveryCrew]

    def get_object(self):
        return self.request.user.delivery_profile


class AssignOrderView(generics.CreateAPIView):
    """Allows Managers to assign an order to a delivery partner."""

    serializer_class = DeliveryAssignmentSerializer
    permission_classes = [IsAuthenticated, IsManager]

    def perform_create(self, serializer):
        assignment = serializer.save()
        # Set partner status to ON_DELIVERY when assigned
        partner = assignment.partner
        partner.status = DeliveryPartner.PartnerStatus.ON_DELIVERY
        partner.save()


class DeliveryAssignmentDetailView(generics.RetrieveUpdateAPIView):
    """Allows Delivery Crew to update the delivery status of an order."""

    serializer_class = DeliveryAssignmentSerializer
    permission_classes = [IsAuthenticated, IsDeliveryCrew]

    def get_queryset(self):
        return DeliveryAssignment.objects.filter(
            partner__user=self.request.user
        ).select_related("order", "partner__user")

    def perform_update(self, serializer):
        assignment = serializer.save()

        # If delivered, mark order fulfilled & release partner back to AVAILABLE
        if assignment.status == DeliveryAssignment.AssignmentStatus.DELIVERED:
            assignment.order.status = Order.StatusChoices.DELIVERED
            assignment.order.save()

            partner = assignment.partner
            partner.status = DeliveryPartner.PartnerStatus.AVAILABLE
            partner.save()
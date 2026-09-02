from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer
from apps.core.permissions import IsManager
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from apps.core.constants import DELIVERY_CREW_GROUP, KITCHEN_STAFF_GROUP, MANAGER_GROUP
from apps.core.permissions import IsDeliveryCrew, IsKitchenStaff, IsManager


# Create your views here.
class OrderView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Order.objects.select_related("user", "delivery_crew").prefetch_related("items__menu_item")

        # Superuser or Manager: full visibility
        if user.is_superuser or user.groups.filter(name=MANAGER_GROUP).exists():
            return queryset.all()

        # Kitchen Staff: pending orders that need preparation
        if user.groups.filter(name=KITCHEN_STAFF_GROUP).exists():
            return queryset.filter(status=False)

        # Delivery Crew: only assigned orders
        if user.groups.filter(name=DELIVERY_CREW_GROUP).exists():
            return queryset.filter(delivery_crew=user)

        # Customers: only their own orders
        return queryset.filter(user=user)


class SingleOrderView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Order.objects.select_related("user", "delivery_crew").prefetch_related("items__menu_item")

        if user.is_superuser or user.groups.filter(name=MANAGER_GROUP).exists():
            return queryset.all()

        if user.groups.filter(name=DELIVERY_CREW_GROUP).exists():
            return queryset.filter(delivery_crew=user)

        return queryset.filter(user=user)

    def patch(self, request, *args, **kwargs):
        user = request.user

        # Delivery crew can only update the status field
        if not (user.is_superuser or user.groups.filter(name=MANAGER_GROUP).exists()):
            if user.groups.filter(name=DELIVERY_CREW_GROUP).exists():
                allowed_fields = {"status"}
                incoming_fields = set(request.data.keys())
                if not incoming_fields.issubset(allowed_fields):
                    return Response(
                        {"detail": "Delivery crew can only update the order status."},
                        status=status.HTTP_403_FORBIDDEN,
                    )

        return super().patch(request, *args, **kwargs)


class OrderItemsView(generics.ListAPIView):
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        order_id = self.kwargs.get("pk")
        queryset = OrderItem.objects.filter(order_id=order_id).select_related("menu_item", "order")

        # Superuser or Manager
        if user.is_superuser or user.groups.filter(name=MANAGER_GROUP).exists():
            return queryset

        # Delivery Crew assigned to the order
        if user.groups.filter(name=DELIVERY_CREW_GROUP).exists():
            return queryset.filter(order__delivery_crew=user)

        # Customer who placed the order
        return queryset.filter(order__user=user)
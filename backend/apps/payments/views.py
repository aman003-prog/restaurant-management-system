from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Payment
from .serializers import PaymentSerializer

# Create your views here.
class ProcessPaymentView(generics.CreateAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        order = serializer.validated_data["order"]
        payment_method = serializer.validated_data.get("payment_method", Payment.PaymentMethod.CARD)

        # Create or update existing payment record for this order
        payment, created = Payment.objects.get_or_create(
            order=order,
            defaults={
                "amount": order.total,
                "payment_method": payment_method,
                "status": Payment.PaymentStatus.COMPLETED,  # Mocked as successful
            },
        )

        if not created:
            payment.amount = order.total
            payment.payment_method = payment_method
            payment.status = Payment.PaymentStatus.COMPLETED
            payment.save()

        # Update order status once payment is confirmed
        order.status = True
        order.save()

        return Response(
            PaymentSerializer(payment, context={"request": request}).data,
            status=status.HTTP_201_CREATED,
        )


class PaymentDetailView(generics.RetrieveAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Payment.objects.filter(order__user=self.request.user).select_related("order")
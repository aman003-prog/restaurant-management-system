from rest_framework import serializers
from apps.orders.models import Order
from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    order = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all())

    class Meta:
        model = Payment
        fields = [
            "id",
            "order",
            "amount",
            "status",
            "transaction_id",
            "payment_method",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "amount",
            "status",
            "transaction_id",
            "created_at",
        ]

    def validate_order(self, value):
        # 1. Verify that order belongs to the requesting user
        user = self.context["request"].user
        if value.user != user:
            raise serializers.ValidationError("You do not own this order.")

        # 2. Prevent duplicate payments on already paid orders
        if hasattr(value, "payment") and value.payment.status == Payment.PaymentStatus.COMPLETED:
            raise serializers.ValidationError("This order has already been paid.")

        return value

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["order"] = f"Order #{instance.order.id}"
        return representation
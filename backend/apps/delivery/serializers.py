from rest_framework import serializers

from apps.orders.models import Order

from .models import DeliveryAssignment, DeliveryPartner


class DeliveryPartnerSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = DeliveryPartner
        fields = [
            "id",
            "user",
            "vehicle_number",
            "government_id",
            "status",
            "created_at",
        ]
        read_only_fields = ["id", "user", "created_at"]


class DeliveryAssignmentSerializer(serializers.ModelSerializer):
    order = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all())
    partner = serializers.PrimaryKeyRelatedField(
        queryset=DeliveryPartner.objects.all()
    )

    class Meta:
        model = DeliveryAssignment
        fields = [
            "id",
            "order",
            "partner",
            "status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["order"] = f"Order #{instance.order.id}"
        representation["partner"] = instance.partner.user.username
        return representation
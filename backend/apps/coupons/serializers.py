from django.utils import timezone
from rest_framework import serializers
from .models import Coupon


class CouponSerializer(serializers.ModelSerializer):
    is_valid = serializers.BooleanField(read_only=True)

    class Meta:
        model = Coupon
        fields = [
            "id",
            "code",
            "discount_type",
            "discount_value",
            "max_discount_amount",
            "min_order_amount",
            "valid_from",
            "valid_until",
            "is_active",
            "is_valid",
            "created_at",
        ]
        read_only_fields = ["id", "is_valid", "created_at"]

    def validate(self, attrs):
        valid_from = attrs.get("valid_from", timezone.now())
        valid_until = attrs.get("valid_until")

        if valid_until and valid_until <= valid_from:
            raise serializers.ValidationError(
                {"valid_until": "Expiration date must be after the start date."}
            )
        return attrs


class ApplyCouponSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=20)
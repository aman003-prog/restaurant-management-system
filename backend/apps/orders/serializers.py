from rest_framework import serializers
from .models import Order, OrderItem
from apps.menu.models import MenuItem
from django.db import transaction
from apps.cart.models import Cart
from apps.coupons.models import Coupon

class OrderItemSerializer(serializers.ModelSerializer):
    menu_item = serializers.PrimaryKeyRelatedField(queryset=MenuItem.objects.all())
    
    class Meta:
        model = OrderItem
        fields = [
            "id",
            "order",
            "menu_item",
            "quantity",
            "unit_price",
            "price",
        ]
        read_only_fields = [
            "id",
            "order",
            "unit_price",
            "price",
        ]

    def to_representation(self, instance):
        """Converts category ID to string title when returning GET responses."""
        representation = super().to_representation(instance)
        representation["order"] = f"Order #{instance.order.id}" if instance.order else None
        representation["menu_item"] = instance.menu_item.title if instance.menu_item else None
        return representation
    
class OrderSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    items = OrderItemSerializer(many=True, read_only=True)
    coupon_code = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "user",
            "delivery_crew",
            "status",
            "total",
            "items",
            "coupon_code",
        ]
        read_only_fields = [
            "id",
            "user",
            "total",
            "items",
        ]

    def to_representation(self, instance):
        """Converts category ID to string title when returning GET responses."""
        representation = super().to_representation(instance)
        representation["user"] = instance.user.username if instance.user else None
        return representation

    def create(self, validated_data):
        user = validated_data["user"]
        coupon_code = validated_data.pop("coupon_code", None)

        with transaction.atomic():
            cart_items = Cart.objects.filter(user=user)
            if not cart_items.exists():
                raise serializers.ValidationError({"detail": "Cart is empty."})

            # Calculate base cart subtotal
            cart_subtotal = sum(item.price for item in cart_items)

            # Validate coupon if provided
            coupon_obj = None
            discount_amount = 0.00

            if coupon_code:
                code_formatted = coupon_code.strip().upper()
                try:
                    coupon_obj = Coupon.objects.get(code=code_formatted)
                except Coupon.DoesNotExist:
                    raise serializers.ValidationError(
                        {"coupon_code": "Invalid coupon code."}
                    )

                if not coupon_obj.is_valid:
                    raise serializers.ValidationError(
                        {"coupon_code": "This coupon is inactive or expired."}
                    )

                if cart_subtotal < coupon_obj.min_order_amount:
                    raise serializers.ValidationError(
                        {
                            "coupon_code": f"Minimum order total of {coupon_obj.min_order_amount} required for this coupon."
                        }
                    )

                discount_amount = coupon_obj.calculate_discount(cart_subtotal)

            final_total = max(cart_subtotal - discount_amount, 0)

            # Create Order instance with discount metadata
            order = Order.objects.create(
                user=user,
                coupon=coupon_obj,
                discount_amount=discount_amount,
                total=final_total,
            )

            # Copy cart items to order items
            order_items = [
                OrderItem(
                    order=order,
                    menu_item=item.menu_item,
                    quantity=item.quantity,
                    unit_price=item.unit_price,
                    price=item.price,
                )
                for item in cart_items
            ]

            OrderItem.objects.bulk_create(order_items)
            cart_items.delete()

            return order
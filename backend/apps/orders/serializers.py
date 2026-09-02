from rest_framework import serializers
from .models import Order, OrderItem
from apps.menu.models import MenuItem
from django.db import transaction
from apps.cart.models import Cart

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
    class Meta:
        model = Order
        fields = [
            "id",
            "user",
            "delivery_crew",
            "status",
            "total",
            "items",
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
        
        with transaction.atomic():
            cart_items = Cart.objects.filter(user=user)
            if not cart_items.exists():
                raise serializers.ValidationError({"detail": "Cart is empty."})

            order = Order.objects.create(user=user, total=0)
            
            total = 0
            order_items = []
            for item in cart_items:
                total += item.price
                order_items.append(OrderItem(order=order, menu_item=item.menu_item, quantity=item.quantity, unit_price=item.unit_price, price=item.price, ))

            OrderItem.objects.bulk_create(order_items)
            order.total = total
            order.save()
            cart_items.delete()

            return order
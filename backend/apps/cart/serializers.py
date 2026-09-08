from django.db import transaction
from django.db.models import F
from rest_framework import serializers

from apps.menu.models import MenuItem
from .models import Cart

class CartSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    menu_item = serializers.PrimaryKeyRelatedField(queryset=MenuItem.objects.all())

    class Meta:
        model = Cart
        fields = [
            "id",
            "user",
            "menu_item",
            "quantity",
            "unit_price",
            "price",
        ]
        read_only_fields = [
            "id",
            "unit_price",
            "price",
        ]

    def to_representation(self, instance):
        """Converts category ID to string title when returning GET responses."""
        representation = super().to_representation(instance)
        representation["user"] = instance.user.username if instance.user else None
        representation["menu_item"] = {
            "id": instance.menu_item.id,
            "title": instance.menu_item.title,
            "price": str(instance.menu_item.price),
            "image": instance.menu_item.item_image.url if instance.menu_item.item_image else None,
            "slug": instance.menu_item.slug,
        }
        return representation

    def validate_menu_item(self, value):
        """Verify that the selected menu item is available."""
        # Assuming your MenuItem model has an 'available' or 'is_available' boolean field
        if not getattr(value, "available", True):
            raise serializers.ValidationError(
                "This menu item is currently unavailable."
            )
        return value

    def create(self, validated_data):
        user = validated_data["user"]
        menu_item = validated_data["menu_item"]
        quantity = validated_data.get("quantity", 1)

        with transaction.atomic():
            cart_item, created = Cart.objects.get_or_create(
                user=user,
                menu_item=menu_item,
                defaults={
                    "quantity": quantity,
                    "unit_price": menu_item.price,
                    "price": menu_item.price * quantity,
                },
            )

            if not created:
                # Update quantity atomically at database level to prevent race conditions
                cart_item.quantity = F("quantity") + quantity
                # Recalculate price using existing unit_price and updated quantity expression
                cart_item.price = F("unit_price") * (F("quantity") + quantity)
                cart_item.save(update_fields=["quantity", "price"])

                # MUST refresh from DB so Python memory replaces F() expressions with actual numeric values
                cart_item.refresh_from_db()

            return cart_item
from rest_framework import serializers
from .models import Cart
from apps.users.models import User
from apps.menu.models import MenuItem

class CartSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
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
        representation["menu_item"] = instance.menu_item.title if instance.menu_item else None
        return representation

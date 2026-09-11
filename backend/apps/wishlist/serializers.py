from rest_framework import serializers
from apps.menu.models import MenuItem
from apps.menu.serializers import MenuItemSerializer
from .models import Wishlist


class WishlistSerializer(serializers.ModelSerializer):
    menu_item = serializers.PrimaryKeyRelatedField(
        queryset=MenuItem.objects.all(), write_only=True
    )
    item = MenuItemSerializer(source="menu_item", read_only=True)

    class Meta:
        model = Wishlist
        fields = ["id", "menu_item", "item", "created_at"]
        read_only_fields = ["id", "item", "created_at"]

    def create(self, validated_data):
        user = self.context["request"].user
        menu_item = validated_data["menu_item"]
        wishlist_item, created = Wishlist.objects.get_or_create(
            user=user, menu_item=menu_item
        )
        return wishlist_item

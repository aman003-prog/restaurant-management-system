from rest_framework import serializers
from apps.menu.models import MenuItem
from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    menu_item = serializers.PrimaryKeyRelatedField(
        queryset=MenuItem.objects.all()
    )

    class Meta:
        model = Review
        fields = [
            "id",
            "user",
            "menu_item",
            "rating",
            "comment",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["user"] = instance.user.username if instance.user else None
        representation["menu_item"] = (
            instance.menu_item.title if instance.menu_item else None
        )
        return representation
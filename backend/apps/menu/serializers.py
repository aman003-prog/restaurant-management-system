from rest_framework import serializers
from .models import MenuItem
from apps.categories.models import Category

class MenuItemSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    class Meta:
        model = MenuItem
        fields = [
            "id",
            "slug",
            "item_image",
            "title",
            "description",
            "price",
            "category",
            "available",
            "preparation_time",
            "calories",
        ]
        read_only_fields = ["id", "slug"]

    def to_representation(self, instance):
        """Converts category ID to string title when returning GET responses."""
        representation = super().to_representation(instance)
        representation["category"] = instance.category.title if instance.category else None
        return representation
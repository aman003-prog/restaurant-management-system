from rest_framework import serializers
from .models import Supplier, Inventory


class SupplierSerializer(serializers.ModelSerializer):
    items_count = serializers.IntegerField(
        source="inventory_items.count", read_only=True
    )

    class Meta:
        model = Supplier
        fields = [
            "id",
            "name",
            "number",
            "email",
            "company_address",
            "items_count",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "items_count", "created_at", "updated_at"]


class InventorySerializer(serializers.ModelSerializer):
    supplier_name = serializers.CharField(
        source="supplier.name", read_only=True, default=None
    )
    is_low_stock = serializers.BooleanField(read_only=True)
    total_value = serializers.FloatField(read_only=True)

    class Meta:
        model = Inventory
        fields = [
            "id",
            "ingredient",
            "quantity",
            "minimum_quantity",
            "maximum_quantity",
            "last_date_of_restock",
            "unit",
            "current_market_price_per_unit",
            "supplier",
            "supplier_name",
            "is_low_stock",
            "total_value",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "supplier_name",
            "is_low_stock",
            "total_value",
            "created_at",
            "updated_at",
        ]

    def validate(self, attrs):
        quantity = attrs.get("quantity", getattr(self.instance, "quantity", 0))
        min_qty = attrs.get(
            "minimum_quantity", getattr(self.instance, "minimum_quantity", 0)
        )
        max_qty = attrs.get(
            "maximum_quantity", getattr(self.instance, "maximum_quantity", 0)
        )

        if min_qty < 0 or max_qty < 0 or quantity < 0:
            raise serializers.ValidationError("Quantities cannot be negative.")

        if max_qty > 0 and min_qty > max_qty:
            raise serializers.ValidationError(
                {"minimum_quantity": "Minimum quantity cannot exceed maximum quantity."}
            )

        return attrs


class RestockSerializer(serializers.Serializer):
    add_quantity = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=0.01)

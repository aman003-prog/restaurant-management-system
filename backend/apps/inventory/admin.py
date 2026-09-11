from django.contrib import admin
from .models import Supplier, Inventory


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "number", "email", "created_at"]
    search_fields = ["name", "email", "number"]


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "ingredient",
        "quantity",
        "unit",
        "minimum_quantity",
        "current_market_price_per_unit",
        "supplier",
        "last_date_of_restock",
    ]
    list_filter = ["unit", "supplier"]
    search_fields = ["ingredient"]

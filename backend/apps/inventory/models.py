from django.db import models
from apps.core.models import TimeStampedModel


class Supplier(TimeStampedModel):
    name = models.CharField(max_length=150)
    number = models.CharField(max_length=20)
    email = models.EmailField()
    company_address = models.TextField()

    def __str__(self):
        return f"{self.name} ({self.number})"

    class Meta:
        ordering = ["name"]


class Inventory(TimeStampedModel):
    ingredient = models.CharField(max_length=150, unique=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    minimum_quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    maximum_quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    last_date_of_restock = models.DateField(null=True, blank=True)
    unit = models.CharField(max_length=50)  # e.g., kg, g, L, ml, pcs, packet
    current_market_price_per_unit = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="inventory_items",
    )

    @property
    def is_low_stock(self):
        return self.quantity <= self.minimum_quantity

    @property
    def total_value(self):
        return round(float(self.quantity) * float(self.current_market_price_per_unit), 2)

    def __str__(self):
        return f"{self.ingredient} ({self.quantity} {self.unit})"

    class Meta:
        verbose_name = "Inventory"
        verbose_name_plural = "Inventories"
        ordering = ["ingredient"]

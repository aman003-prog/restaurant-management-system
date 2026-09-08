from django.db import models
from apps.core.models import TimeStampedModel
from django.conf import settings
from apps.menu.models import MenuItem
from apps.cart.models import Cart

# Create your models here.
class Order(TimeStampedModel):
    class StatusChoices(models.TextChoices):
        PENDING_PAYMENT = "PENDING_PAYMENT", "Pending Payment"
        CONFIRMED = "CONFIRMED", "Confirmed"
        PREPARING = "PREPARING", "Preparing in Kitchen"
        READY_FOR_PICKUP = "READY_FOR_PICKUP", "Ready for Pickup"
        OUT_FOR_DELIVERY = "OUT_FOR_DELIVERY", "Out for Delivery"
        DELIVERED = "DELIVERED", "Delivered"
        CANCELLED = "CANCELLED", "Cancelled"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    delivery_crew = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name="delivery_crew", null=True, blank=True, )
    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.PENDING_PAYMENT,
    )
    coupon = models.ForeignKey(
        "coupons.Coupon",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="orders",
    )
    discount_amount = models.DecimalField(
        max_digits=6, decimal_places=2, default=0.00
    )
    total = models.DecimalField(max_digits=6, decimal_places=2, default=0.00, )

    def __str__(self):
        return f"Order #{self.id} - {self.user.username} ({self.total})"

    class Meta:
        ordering = ["-created_at"]

class OrderItem(TimeStampedModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items", )
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=1, )
    unit_price = models.DecimalField(max_digits=6, decimal_places=2, )
    price = models.DecimalField(max_digits=6, decimal_places=2, )

    def __str__(self):
        return f"{self.order.user.username} - {self.order}"
        
    class Meta:
        ordering = ["order"]
        constraints = [
            models.UniqueConstraint(
                fields=["order", "menu_item"],
                name="unique_order_menu-item",
            ),
        ]

    def save(self, *args, **kwargs):
        self.unit_price = self.menu_item.price
        self.price = self.unit_price * self.quantity
        return super().save(*args, **kwargs)
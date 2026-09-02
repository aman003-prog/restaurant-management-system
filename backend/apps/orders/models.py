from django.db import models
from apps.core.models import TimeStampedModel
from django.conf import settings
from apps.menu.models import MenuItem
from apps.cart.models import Cart

# Create your models here.
class Order(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    delivery_crew = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name="delivery_crew", null=True, blank=True, )
    status = models.BooleanField(default=False, )   #Later need to change it to the dropdown with various options
    total = models.DecimalField(max_digits=6, decimal_places=2, default=0.00, )

    def __str__(self):
            return f"{self.user.username} - {self.status}({self.total})"
    
    class Meta:
        ordering = ["user"]

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
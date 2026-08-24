from django.db import models
from apps.core.models import TimeStampedModel
from django.conf import settings
from apps.menu.models import MenuItem

# Create your models here.
class Cart(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=1, )
    unit_price = models.DecimalField(max_digits=6, decimal_places=2, )
    price = models.DecimalField(max_digits=6, decimal_places=2, )

    def __str__(self):
        return f"{self.user.username} - {self.menu_item}({self.quantity})"

    class Meta:
        ordering = ["menu_item"]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "menu_item"],
                name="unique_user_menu-item",
            ),
        ]

    def save(self, *args, **kwargs):
        self.unit_price = self.menu_item.price
        self.price = self.unit_price * self.quantity
        return super().save(*args, **kwargs)
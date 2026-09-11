from django.db import models
from django.conf import settings
from apps.core.models import TimeStampedModel
from apps.menu.models import MenuItem


class Wishlist(TimeStampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="wishlist_items",
    )
    menu_item = models.ForeignKey(
        MenuItem,
        on_delete=models.CASCADE,
        related_name="wishlisted_by",
    )

    def __str__(self):
        return f"{self.user.username} - {self.menu_item.title}"

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "menu_item"],
                name="unique_user_menu_item_wishlist",
            )
        ]

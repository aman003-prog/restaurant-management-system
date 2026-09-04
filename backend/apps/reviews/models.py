from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from apps.core.models import TimeStampedModel
from apps.menu.models import MenuItem

# Create your models here.
class Review(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(
        MenuItem, on_delete=models.CASCADE, related_name="reviews"
    )
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField(blank=True, default="")

    def __str__(self):
        return f"{self.user.username} - {self.menu_item.title} ({self.rating}/5)"

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "menu_item"],
                name="unique_user_menu_item_review",
            )
        ]
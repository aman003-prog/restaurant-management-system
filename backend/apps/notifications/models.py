from django.db import models
from django.conf import settings


class Notification(models.Model):
    TYPE_CHOICES = [
        ("order", "Order Update"),
        ("inventory", "Inventory Alert"),
        ("promo", "Promotion"),
        ("system", "System Notice"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications",
    )
    type = models.CharField(max_length=50, choices=TYPE_CHOICES, default="system")
    message = models.TextField()
    read_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.type}] {self.user.username}: {self.message[:30]}"

    class Meta:
        ordering = ["-created_at"]

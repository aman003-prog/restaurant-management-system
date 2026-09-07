from django.db import models
from django.conf import settings
from django.db import models

from apps.core.models import TimeStampedModel
from apps.orders.models import Order

# Create your models here.
class DeliveryPartner(TimeStampedModel):
    class PartnerStatus(models.TextChoices):
        AVAILABLE = "AVAILABLE", "Available"
        ON_DELIVERY = "ON_DELIVERY", "On Delivery"
        OFFLINE = "OFFLINE", "Offline"

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="delivery_profile",
    )
    vehicle_number = models.CharField(max_length=30)
    government_id = models.CharField(
        max_length=50,
        unique=True,
        help_text="Driver's License, Aadhaar, or National ID",
    )
    status = models.CharField(
        max_length=20,
        choices=PartnerStatus.choices,
        default=PartnerStatus.OFFLINE,
    )

    def __str__(self):
        return f"{self.user.username} ({self.vehicle_number}) - {self.status}"

    class Meta:
        ordering = ["-created_at"]


class DeliveryAssignment(TimeStampedModel):
    class AssignmentStatus(models.TextChoices):
        ASSIGNED = "ASSIGNED", "Assigned"
        PICKED_UP = "PICKED_UP", "Picked Up"
        DELIVERED = "DELIVERED", "Delivered"
        CANCELLED = "CANCELLED", "Cancelled"

    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name="delivery_assignment",
    )
    partner = models.ForeignKey(
        DeliveryPartner,
        on_delete=models.CASCADE,
        related_name="assignments",
    )
    status = models.CharField(
        max_length=20,
        choices=AssignmentStatus.choices,
        default=AssignmentStatus.ASSIGNED,
    )

    def __str__(self):
        return f"Order #{self.order.id} -> {self.partner.user.username} ({self.status})"

    class Meta:
        ordering = ["-created_at"]
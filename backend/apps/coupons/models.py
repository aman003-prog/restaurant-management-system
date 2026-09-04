from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from apps.core.models import TimeStampedModel

# Create your models here.
class Coupon(TimeStampedModel):
    class DiscountType(models.TextChoices):
        PERCENTAGE = "PERCENTAGE", "Percentage"
        FLAT = "FLAT", "Flat Amount"

    code = models.CharField(max_length=20, unique=True)
    discount_type = models.CharField(
        max_length=10,
        choices=DiscountType.choices,
        default=DiscountType.PERCENTAGE,
    )
    discount_value = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        help_text="Percentage value (1-100) or flat amount off",
    )
    max_discount_amount = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Cap on maximum discount for percentage coupons (optional)",
    )
    min_order_amount = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=0.00,
        help_text="Minimum cart total required to apply coupon",
    )
    valid_from = models.DateTimeField(default=timezone.now)
    valid_until = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        self.code = self.code.upper().strip()
        super().save(*args, **kwargs)

    @property
    def is_valid(self):
        now = timezone.now()
        return self.is_active and self.valid_from <= now <= self.valid_until

    def calculate_discount(self, order_total):
        """Calculates discount amount based on order total."""
        if not self.is_valid or order_total < self.min_order_amount:
            return 0.00

        if self.discount_type == self.DiscountType.FLAT:
            return min(self.discount_value, order_total)

        if self.discount_type == self.DiscountType.PERCENTAGE:
            calculated_discount = (order_total * self.discount_value) / 100
            if self.max_discount_amount:
                return min(calculated_discount, self.max_discount_amount)
            return calculated_discount

        return 0.00

    def __str__(self):
        return f"{self.code} ({self.discount_value}{'%' if self.discount_type == self.DiscountType.PERCENTAGE else ' OFF'})"

    class Meta:
        ordering = ["-created_at"]
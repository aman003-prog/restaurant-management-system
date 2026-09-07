from django.db import models
import uuid
from django.db import models
from apps.core.models import TimeStampedModel
from apps.orders.models import Order

# Create your models here.
class Payment(TimeStampedModel):
    class PaymentStatus(models.TextChoices):
        PENDING = "PENDING", "Pending"
        COMPLETED = "COMPLETED", "Completed"
        FAILED = "FAILED", "Failed"
        REFUNDED = "REFUNDED", "Refunded"

    class PaymentMethod(models.TextChoices):
        CARD = "CARD", "Credit/Debit Card"
        UPI = "UPI", "UPI"
        NET_BANKING = "NET_BANKING", "Net Banking"
        COD = "COD", "Cash on Delivery"
        STRIPE = "STRIPE", "Stripe"
        RAZORPAY = "RAZORPAY", "Razorpay"

    order = models.OneToOneField(
        Order, on_delete=models.CASCADE, related_name="payment"
    )
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING,
    )
    transaction_id = models.CharField(
        max_length=100, unique=True, blank=True, null=True
    )
    payment_method = models.CharField(
        max_length=20,
        choices=PaymentMethod.choices,
        default=PaymentMethod.CARD,
    )

    def save(self, *args, **kwargs):
        # Generate a mock transaction ID for now if not supplied by a gateway
        if not self.transaction_id:
            self.transaction_id = f"TXN-{uuid.uuid4().hex[:12].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Payment #{self.id} - Order #{self.order.id} ({self.status})"

    class Meta:
        ordering = ["-created_at"]
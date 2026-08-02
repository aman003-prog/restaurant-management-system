from django.db import models
from core.models import TimeStampedModel
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser, TimeStampedModel):
    profile_image = models.ImageField(blank=True, upload_to="users/profile_images", )     #User can add image if want to other wise it will be empty
    phone_number = models.CharField(null=True, unique=True, blank=True, max_length=15, )     #User need to add a mobile number right now 10 digits indian number
    date_of_birth = models.DateField(null=True, blank=True, )      #format DD-MM-YYYY 
    email = models.EmailField(unique=True, )       #unique email

    def __str__(self):
        return f"{self.username}"

    class Meta:
        ordering = ["username"]

class Address(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="addresses", )
    label = models.CharField(max_length=30)
    address = models.TextField()
    city = models.CharField(max_length=255)     #will later change to dropdown or options
    state = models.CharField(max_length=255)     #will later change to dropdown or options
    country = models.CharField(max_length=255)     #will later change to dropdown or options
    postal_code = models.CharField(max_length=20)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.label} ({self.user.username})"

    class Meta:
        ordering = ["label"]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "label"],
                name="unique_user_label",
            ),
            models.UniqueConstraint(
                fields=["user"],
                condition=models.Q(is_default=True),
                name="unique_default_address",
            ),
        ]
from rest_framework import serializers
from .models import User, Address

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "date_of_birth",
            "profile_image",
            "is_active",
        ]


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = [
            "label",
            "address",
            "city",
            "state",
            "country",
            "postal_code",
            "is_default",
        ]
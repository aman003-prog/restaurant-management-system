from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import User, Address
from .serializers import UserProfileSerializer, AddressSerializer
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
class UserProfileView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()

    def get_object(self):
        return self.request.user

    def delete(self, request, *args, **kwargs):
        return Response(
            {
                "detail": (
                    "Account deletion is temporarily disabled. "
                    "This feature will require password confirmation "
                    "and/or email verification."
                )
            },
            status=status.HTTP_403_FORBIDDEN,
        )

class AddressView(generics.ListCreateAPIView):
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        if serializer.validated_data["is_default"]:
            Address.objects.filter(
                user=self.request.user,
                is_default=True
            ).update(is_default=False)

        serializer.save(user=self.request.user)

class SingleAddressView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Address.objects.filter(user = self.request.user)

    def perform_update(self, serializer):
        if serializer.validated_data.get("is_default"):
            Address.objects.filter(
                user=self.request.user,
                is_default=True
            ).exclude(pk=serializer.instance.pk).update(is_default = False)

        serializer.save()

    def delete(self, request, *args, **kwargs):
        return Response(
            {
                "detail": (
                    "Address deletion is temporarily disabled. "
                    "This feature will require password confirmation "
                    "and/or email verification."
                )
            },
            status=status.HTTP_403_FORBIDDEN,
        )
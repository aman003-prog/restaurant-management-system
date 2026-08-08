from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Cart
from .serializers import CartSerializer
from apps.core.permissions import IsManager
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from apps.core.constants import SAFE_METHODS

# Create your views here.
class CartView(generics.ListCreateAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

class SingleCartItemView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)
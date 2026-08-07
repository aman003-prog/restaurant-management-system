from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import MenuItem
from .serializers import MenuItemSerializer
from apps.core.permissions import IsManager
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from apps.core.constants import SAFE_METHODS

# Create your views here.
class MenuItemView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ["available"]
    search_fields = ["title", "description",]
    ordering_fields = ["title", "created_at"]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and user.is_staff:
            return MenuItem.objects.all().select_related("category")
        return MenuItem.objects.filter(available=True).select_related("category")

    def get_permissions(self):
        if(self.request.method in SAFE_METHODS):
            return [AllowAny()]
        return [IsManager()]

class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = "slug"
    queryset = MenuItem.objects.all().select_related("category")
    serializer_class = MenuItemSerializer

    def get_permissions(self):
            if(self.request.method in SAFE_METHODS):
                return [AllowAny()]
            return [IsManager()]
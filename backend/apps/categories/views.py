from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import Category
from .serializers import CategorySerializer
from apps.core.permissions import IsManager
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

# Create your views here.
class CategoriesView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ["is_active"]
    search_fields = ["title", "description",]
    ordering_fields = ["title", "created_at"]

    def get_queryset(self):
        return Category.objects.filter(is_active=True)

    def get_permissions(self):
        if(self.request.method=='GET'):
            return [AllowAny()]
        return [IsManager()]
    
class SingleCategoryView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = "slug"
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if(self.request.method=='GET'):
            return [AllowAny()]
        return [IsManager()]
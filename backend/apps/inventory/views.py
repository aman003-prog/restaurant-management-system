from django.utils import timezone
from rest_framework import generics, status
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import Supplier, Inventory
from .serializers import SupplierSerializer, InventorySerializer, RestockSerializer


class IsStaffOrManager(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and (
                request.user.is_staff
                or request.user.is_superuser
                or request.user.groups.filter(name="Manager").exists()
            )
        )


class SupplierListCreateView(generics.ListCreateAPIView):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [IsStaffOrManager]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["name", "email", "number", "company_address"]
    ordering_fields = ["name", "created_at"]


class SupplierDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [IsStaffOrManager]


class InventoryListCreateView(generics.ListCreateAPIView):
    serializer_class = InventorySerializer
    permission_classes = [IsStaffOrManager]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["supplier"]
    search_fields = ["ingredient", "unit"]
    ordering_fields = ["ingredient", "quantity", "current_market_price_per_unit", "created_at"]

    def get_queryset(self):
        queryset = Inventory.objects.select_related("supplier").all()
        low_stock = self.request.query_params.get("low_stock")
        if low_stock is not None:
            if low_stock.lower() in ["true", "1"]:
                from django.db.models import F
                queryset = queryset.filter(quantity__lte=F("minimum_quantity"))
        return queryset


class InventoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Inventory.objects.select_related("supplier").all()
    serializer_class = InventorySerializer
    permission_classes = [IsStaffOrManager]


class InventoryRestockView(generics.GenericAPIView):
    queryset = Inventory.objects.all()
    serializer_class = RestockSerializer
    permission_classes = [IsStaffOrManager]

    def post(self, request, pk=None):
        inventory_item = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        add_qty = serializer.validated_data["add_quantity"]
        inventory_item.quantity += add_qty
        inventory_item.last_date_of_restock = timezone.now().date()
        inventory_item.save(update_fields=["quantity", "last_date_of_restock", "updated_at"])

        return Response(
            InventorySerializer(inventory_item).data,
            status=status.HTTP_200_OK,
        )

from django.urls import path
from . import views

urlpatterns = [
    path("suppliers/", views.SupplierListCreateView.as_view(), name="supplier-list-create"),
    path("suppliers/<int:pk>/", views.SupplierDetailView.as_view(), name="supplier-detail"),
    path("inventory/", views.InventoryListCreateView.as_view(), name="inventory-list-create"),
    path("inventory/<int:pk>/", views.InventoryDetailView.as_view(), name="inventory-detail"),
    path("inventory/<int:pk>/restock/", views.InventoryRestockView.as_view(), name="inventory-restock"),
]

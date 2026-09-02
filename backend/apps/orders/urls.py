from django.urls import path
from . import views

urlpatterns = [
    path("orders/", views.OrderView.as_view(), name="order-list"),
    path("orders/<int:pk>/", views.SingleOrderView.as_view(), name="order-detail"),
    path("orders/<int:pk>/items/", views.OrderItemsView.as_view(), name="order-items-list", ),
]
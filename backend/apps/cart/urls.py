from django.urls import path
from . import views

urlpatterns = [
    path("cart/", views.CartView.as_view(), name="cart"),
    path("cart/<int:pk>/", views.SingleCartItemView.as_view(), name="cart-items"),
]
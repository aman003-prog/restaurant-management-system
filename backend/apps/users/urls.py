from django.urls import path
from . import views

urlpatterns = [
    path('users/me/', views.UserProfileView.as_view(), name="user-profile"),
    path('users/addresses/', views.AddressView.as_view(), name="address"),
    path('users/addresses/<int:pk>/', views.SingleAddressView.as_view(), name="single-address"),
]
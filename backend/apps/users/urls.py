from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("auth/register/", views.RegisterView.as_view(), name="register"),
    path("auth/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path('users/me/', views.UserProfileView.as_view(), name="user-profile"),
    path('users/addresses/', views.AddressView.as_view(), name="address"),
    path('users/addresses/<int:pk>/', views.SingleAddressView.as_view(), name="single-address"),
]
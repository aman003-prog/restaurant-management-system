from django.urls import path
from . import views

urlpatterns = [
    path("menu-items/", views.MenuItemView.as_view(), name="menu-item"),
    path("menu-item/<slug:slug>/", views.SingleMenuItemView.as_view(), name="menu-item-detail"),
]
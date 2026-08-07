from django.urls import path
from . import views

urlpatterns = [
    path("menuitems/", views.MenuItemView.as_view(), name="menu-item"),
    path("menuitem/<slug:slug>/", views.SingleMenuItemView.as_view(), name="menu-item-detail"),
]
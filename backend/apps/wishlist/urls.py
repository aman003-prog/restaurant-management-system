from django.urls import path
from . import views

urlpatterns = [
    path("wishlist/", views.WishlistListCreateView.as_view(), name="wishlist-list-create"),
    path("wishlist/<int:pk>/", views.WishlistDestroyView.as_view(), name="wishlist-destroy"),
    path("wishlist/toggle/", views.WishlistToggleView.as_view(), name="wishlist-toggle"),
]

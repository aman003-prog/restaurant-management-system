from django.urls import path
from . import views

urlpatterns = [
    path("menu-items/<int:menu_item_id>/reviews/", views.MenuItemReviewListCreateView.as_view(), name="menu-item-reviews"),
    path("reviews/mine/", views.UserReviewListView.as_view(), name="user-reviews"),
    path("reviews/<int:pk>/", views.SingleReviewDetailView.as_view(), name="review-detail"),
]
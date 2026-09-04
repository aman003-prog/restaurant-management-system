from django.shortcuts import render
from rest_framework import generics, serializers, status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from apps.menu.models import MenuItem
from .models import Review
from .serializers import ReviewSerializer

# Create your views here.
class MenuItemReviewListCreateView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        menu_item_id = self.kwargs.get("menu_item_id")
        return Review.objects.filter(menu_item_id=menu_item_id).select_related("user", "menu_item")

    def perform_create(self, serializer):
        menu_item_id = self.kwargs.get("menu_item_id")
        
        # Verify menu item exists
        if not MenuItem.objects.filter(id=menu_item_id).exists():
            raise serializers.ValidationError({"detail": "Menu item not found."})

        # Check if user has already reviewed this item
        if Review.objects.filter(user=self.request.user, menu_item_id=menu_item_id).exists():
            raise serializers.ValidationError({"detail": "You have already reviewed this menu item."})

        serializer.save(user=self.request.user, menu_item_id=menu_item_id)


class UserReviewListView(generics.ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Review.objects.filter(user=self.request.user).select_related("menu_item")


class SingleReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Users can only modify or delete their own reviews
        return Review.objects.filter(user=self.request.user).select_related("menu_item")
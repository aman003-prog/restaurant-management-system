from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.menu.models import MenuItem
from .models import Wishlist
from .serializers import WishlistSerializer


class WishlistListCreateView(generics.ListCreateAPIView):
    serializer_class = WishlistSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            Wishlist.objects.filter(user=self.request.user)
            .select_related("menu_item", "menu_item__category")
            .all()
        )

    def perform_create(self, serializer):
        serializer.save()


class WishlistDestroyView(generics.DestroyAPIView):
    serializer_class = WishlistSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user)


class WishlistToggleView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        menu_item_id = request.data.get("menu_item") or request.data.get("menu_item_id")
        if not menu_item_id:
            return Response(
                {"detail": "menu_item is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            menu_item = MenuItem.objects.get(id=menu_item_id)
        except MenuItem.DoesNotExist:
            return Response(
                {"detail": "Menu item not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        existing = Wishlist.objects.filter(user=request.user, menu_item=menu_item).first()
        if existing:
            existing.delete()
            return Response(
                {"status": "removed", "menu_item_id": menu_item.id},
                status=status.HTTP_200_OK,
            )
        else:
            new_item = Wishlist.objects.create(user=request.user, menu_item=menu_item)
            return Response(
                {
                    "status": "added",
                    "menu_item_id": menu_item.id,
                    "item": WishlistSerializer(new_item, context={"request": request}).data,
                },
                status=status.HTTP_201_CREATED,
            )

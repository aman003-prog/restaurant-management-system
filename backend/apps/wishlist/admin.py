from django.contrib import admin
from .models import Wishlist


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "menu_item", "created_at"]
    list_filter = ["created_at"]
    search_fields = ["user__username", "menu_item__title"]

from django.contrib import admin
from .models import UserProfile, WishList, WishListItem


class WishListItemInline(admin.TabularInline):
    model = WishListItem
    extra = 0


@admin.register(WishList)
class WishListAdmin(admin.ModelAdmin):
    list_display = ["user"]
    inlines = [WishListItemInline]


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "default_full_name", "default_town_or_city", "default_country"]
    search_fields = ["user__username", "user__email", "default_full_name"]

from django.contrib import admin
from .models import WishList, WishListItem


class WishListItemInline(admin.TabularInline):
    model = WishListItem
    extra = 0


@admin.register(WishList)
class WishListAdmin(admin.ModelAdmin):
    list_display = ["user"]
    inlines = [WishListItemInline]
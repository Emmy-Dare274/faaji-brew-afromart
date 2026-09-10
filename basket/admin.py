from django.contrib import admin
from .models import Basket, BasketItem


class BasketItemInline(admin.TabularInline):
    model = BasketItem
    extra = 0


@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "session_key", "item_count", "total", "updated_at"]
    inlines = [BasketItemInline]

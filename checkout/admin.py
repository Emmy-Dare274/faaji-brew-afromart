from django.contrib import admin
from .models import Order, OrderLineItem


class OrderLineItemInline(admin.TabularInline):
    model = OrderLineItem
    extra = 0
    readonly_fields = ["lineitem_total"]

    def lineitem_total(self, obj):
        return f"${obj.lineitem_total:.2f}"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["order_number", "user", "status", "grand_total", "created_at"]
    list_filter = ["status"]
    search_fields = ["order_number", "email"]
    readonly_fields = ["order_number", "order_total", "delivery_cost", "grand_total", "stripe_pid"]
    inlines = [OrderLineItemInline]
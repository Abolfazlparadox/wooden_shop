from django.contrib import admin
from .models import Order, OrderItem, CustomOrder


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('variation', 'price', 'quantity')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'phone_number', 'status', 'total_price', 'created_at')
    list_filter = ('status', 'shipping_method', 'payment_method', 'created_at')
    search_fields = ('full_name', 'phone_number', 'address', 'tracking_code')
    inlines = [OrderItemInline]
    readonly_fields = ('created_at',)


@admin.register(CustomOrder)
class CustomOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_name', 'phone_number', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('customer_name', 'phone_number', 'description')
    readonly_fields = ('created_at',)

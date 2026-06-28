from django.contrib import admin
from .models import Order, OrderItem, CustomOrder

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('variation', 'formatted_price', 'quantity')

    def formatted_price(self, obj):
        return f"{obj.price:,} تومان"
    formatted_price.short_description = 'قیمت'

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'phone_number', 'status', 'formatted_total_price', 'created_at')
    list_filter = ('status', 'shipping_method', 'payment_method', 'created_at')
    search_fields = ('full_name', 'phone_number', 'address', 'tracking_code')
    inlines = [OrderItemInline]
    readonly_fields = ('created_at',)

    def formatted_total_price(self, obj):
        return f"{obj.total_price:,} تومان"
    formatted_total_price.short_description = 'مبلغ کل'

@admin.register(CustomOrder)
class CustomOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_name', 'phone_number', 'status', 'formatted_proposed_price', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('customer_name', 'phone_number', 'description')
    readonly_fields = ('created_at',)

    def formatted_proposed_price(self, obj):
        if obj.proposed_price:
            return f"{obj.proposed_price:,} تومان"
        return "-"
    formatted_proposed_price.short_description = 'قیمت پیشنهادی'

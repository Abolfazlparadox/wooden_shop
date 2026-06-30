from django.contrib import admin
from .models import CustomUser, Address, OTP

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'first_name', 'last_name', 'is_staff', 'is_active', 'is_phone_verified')
    list_filter = ('is_staff', 'is_active', 'is_phone_verified')
    search_fields = ('phone_number', 'first_name', 'last_name') # This is required for autocomplete_fields to work
    ordering = ('-date_joined',)

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'state', 'city', 'is_default')
    list_filter = ('state', 'is_default')
    search_fields = ('user__phone_number', 'city', 'full_address')

@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    list_display = ('user', 'code', 'created_at', 'is_used')
    list_filter = ('is_used', 'created_at')
    search_fields = ('user__phone_number',)

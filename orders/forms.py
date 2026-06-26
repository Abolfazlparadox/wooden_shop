from django import forms
from .models import Order

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['full_name', 'phone_number', 'address', 'postal_code', 'shipping_method', 'payment_method']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-walnut-800 focus:ring-walnut-800 sm:text-sm',
                'placeholder': 'نام و نام خانوادگی تحویل‌گیرنده'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-walnut-800 focus:ring-walnut-800 sm:text-sm',
                'placeholder': '09123456789'
            }),
            'address': forms.Textarea(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-walnut-800 focus:ring-walnut-800 sm:text-sm',
                'rows': 3,
                'placeholder': 'آدرس دقیق پستی'
            }),
            'postal_code': forms.TextInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-walnut-800 focus:ring-walnut-800 sm:text-sm',
                'placeholder': 'کد پستی ۱۰ رقمی'
            }),
            'shipping_method': forms.Select(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-walnut-800 focus:ring-walnut-800 sm:text-sm'
            }),
            'payment_method': forms.Select(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-walnut-800 focus:ring-walnut-800 sm:text-sm'
            }),
        }

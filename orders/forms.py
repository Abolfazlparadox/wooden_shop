from django import forms
from .models import Order

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['full_name', 'phone_number', 'address', 'postal_code', 'shipping_method', 'payment_method']
        
        attrs_dict = {
            'class': 'w-full px-4 py-3 rounded-xl border border-slate-200 bg-slate-50 text-slate-800 focus:outline-none focus:ring-2 focus:ring-walnut-800 focus:border-transparent transition-all duration-300 dark:bg-slate-800 dark:border-slate-700 dark:text-white dark:focus:ring-walnut-500'
        }
        
        widgets = {
            'full_name': forms.TextInput(attrs={**attrs_dict, 'placeholder': 'نام و نام خانوادگی تحویل‌گیرنده'}),
            'phone_number': forms.TextInput(attrs={**attrs_dict, 'placeholder': '09123456789'}),
            'address': forms.Textarea(attrs={**attrs_dict, 'rows': 3, 'placeholder': 'آدرس دقیق پستی'}),
            'postal_code': forms.TextInput(attrs={**attrs_dict, 'placeholder': 'کد پستی ۱۰ رقمی'}),
            'shipping_method': forms.Select(attrs=attrs_dict),
            'payment_method': forms.Select(attrs=attrs_dict),
        }

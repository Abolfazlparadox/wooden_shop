from django import forms
from .models import CustomUser, Address

# Define a common attrs dictionary to be reused
attrs_dict = {
    'class': 'w-full px-4 py-3 rounded-xl border border-slate-200 bg-slate-50 text-slate-800 focus:outline-none focus:ring-2 focus:ring-walnut-800 focus:border-transparent transition-all duration-300 dark:bg-slate-800 dark:border-slate-700 dark:text-white dark:focus:ring-walnut-500'
}

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='کلمه عبور', widget=forms.PasswordInput(attrs={**attrs_dict, 'id': 'password-field', 'placeholder': '••••••••'}))
    confirm_password = forms.CharField(label='تکرار کلمه عبور', widget=forms.PasswordInput(attrs={**attrs_dict, 'placeholder': '••••••••'}))

    class Meta:
        model = CustomUser
        fields = ('phone_number', 'first_name', 'last_name')
        widgets = {
            'phone_number': forms.TextInput(attrs={**attrs_dict, 'placeholder': '09123456789'}),
            'first_name': forms.TextInput(attrs={**attrs_dict, 'placeholder': 'نام'}),
            'last_name': forms.TextInput(attrs={**attrs_dict, 'placeholder': 'نام خانوادگی'}),
        }
    # ... (validation methods remain the same)

class UserLoginForm(forms.Form):
    phone_number = forms.CharField(label='شماره تلفن', widget=forms.TextInput(attrs={**attrs_dict, 'placeholder': '09123456789'}))
    password = forms.CharField(label='کلمه عبور', widget=forms.PasswordInput(attrs={**attrs_dict, 'placeholder': '••••••••'}))

class OTPVerifyForm(forms.Form):
    code = forms.CharField(label='کد تایید', max_length=6, widget=forms.TextInput(attrs={**attrs_dict, 'class': attrs_dict['class'] + ' text-center tracking-[1em]', 'placeholder': '------'}))

class ForgotPasswordForm(forms.Form):
    phone_number = forms.CharField(label='شماره تلفن', widget=forms.TextInput(attrs={**attrs_dict, 'placeholder': 'شماره تلفنی که با آن ثبت نام کرده‌اید'}))

class SetNewPasswordForm(forms.Form):
    password = forms.CharField(label='کلمه عبور جدید', widget=forms.PasswordInput(attrs=attrs_dict))
    confirm_password = forms.CharField(label='تکرار کلمه عبور جدید', widget=forms.PasswordInput(attrs=attrs_dict))
    # ... (validation method remains the same)

class ProfileInfoForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name']
        widgets = {
            'first_name': forms.TextInput(attrs=attrs_dict),
            'last_name': forms.TextInput(attrs=attrs_dict),
        }

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['full_name', 'state', 'city', 'postal_code', 'full_address', 'phone_number', 'is_default']
        widgets = {
            'full_name': forms.TextInput(attrs=attrs_dict),
            'state': forms.TextInput(attrs=attrs_dict),
            'city': forms.TextInput(attrs=attrs_dict),
            'postal_code': forms.TextInput(attrs=attrs_dict),
            'full_address': forms.Textarea(attrs={**attrs_dict, 'rows': 3}),
            'phone_number': forms.TextInput(attrs=attrs_dict),
            'is_default': forms.CheckboxInput(attrs={'class': 'h-5 w-5 rounded border-gray-300 text-walnut-800 focus:ring-walnut-700'}),
        }

from django import forms
from .models import CustomUser, Address

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='کلمه عبور', widget=forms.PasswordInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-walnut-800 focus:ring-walnut-800 sm:text-lg p-3 dark:bg-slate-800 dark:border-slate-600', 'id': 'password-field'}))
    confirm_password = forms.CharField(label='تکرار کلمه عبور', widget=forms.PasswordInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-walnut-800 focus:ring-walnut-800 sm:text-lg p-3 dark:bg-slate-800 dark:border-slate-600'}))
    class Meta:
        model = CustomUser
        fields = ('phone_number', 'first_name', 'last_name')
        # ... (rest of the form is the same)

class UserLoginForm(forms.Form):
    phone_number = forms.CharField(label='شماره تلفن', widget=forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-walnut-800 focus:ring-walnut-800 sm:text-lg p-3 dark:bg-slate-800 dark:border-slate-600'}))
    password = forms.CharField(label='کلمه عبور', widget=forms.PasswordInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-walnut-800 focus:ring-walnut-800 sm:text-lg p-3 dark:bg-slate-800 dark:border-slate-600'}))

class OTPVerifyForm(forms.Form):
    code = forms.CharField(label='کد تایید', max_length=6, widget=forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-walnut-800 focus:ring-walnut-800 sm:text-lg p-3 text-center tracking-[1em] dark:bg-slate-800 dark:border-slate-600'}))

class ForgotPasswordForm(forms.Form):
    phone_number = forms.CharField(label='شماره تلفن', widget=forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-walnut-800 focus:ring-walnut-800 sm:text-lg p-3 dark:bg-slate-800 dark:border-slate-600'}))

class SetNewPasswordForm(forms.Form):
    password = forms.CharField(label='کلمه عبور جدید', widget=forms.PasswordInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-walnut-800 focus:ring-walnut-800 sm:text-lg p-3 dark:bg-slate-800 dark:border-slate-600'}))
    confirm_password = forms.CharField(label='تکرار کلمه عبور جدید', widget=forms.PasswordInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-walnut-800 focus:ring-walnut-800 sm:text-lg p-3 dark:bg-slate-800 dark:border-slate-600'}))

class ProfileInfoForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-walnut-800 focus:ring-walnut-800 sm:text-sm dark:bg-slate-700 dark:border-slate-600'}),
            'last_name': forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-walnut-800 focus:ring-walnut-800 sm:text-sm dark:bg-slate-700 dark:border-slate-600'}),
        }

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['full_name', 'state', 'city', 'postal_code', 'full_address', 'phone_number', 'is_default']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-walnut-800 focus:ring-walnut-800 sm:text-sm dark:bg-slate-700 dark:border-slate-600'}),
            'state': forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-walnut-800 focus:ring-walnut-800 sm:text-sm dark:bg-slate-700 dark:border-slate-600'}),
            'city': forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-walnut-800 focus:ring-walnut-800 sm:text-sm dark:bg-slate-700 dark:border-slate-600'}),
            'postal_code': forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-walnut-800 focus:ring-walnut-800 sm:text-sm dark:bg-slate-700 dark:border-slate-600'}),
            'full_address': forms.Textarea(attrs={'rows': 3, 'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-walnut-800 focus:ring-walnut-800 sm:text-sm dark:bg-slate-700 dark:border-slate-600'}),
            'phone_number': forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-walnut-800 focus:ring-walnut-800 sm:text-sm dark:bg-slate-700 dark:border-slate-600'}),
            'is_default': forms.CheckboxInput(attrs={'class': 'h-4 w-4 rounded border-gray-300 text-walnut-800 focus:ring-walnut-700'}),
        }

from django import forms
from .models import CustomUser

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        label='کلمه عبور',
        widget=forms.PasswordInput(attrs={
            'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-walnut-800 focus:ring-walnut-800 sm:text-lg p-3 dark:bg-slate-800 dark:border-slate-600',
            'placeholder': '••••••••',
            'id': 'password-field'
        })
    )
    confirm_password = forms.CharField(
        label='تکرار کلمه عبور',
        widget=forms.PasswordInput(attrs={
            'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-walnut-800 focus:ring-walnut-800 sm:text-lg p-3 dark:bg-slate-800 dark:border-slate-600',
            'placeholder': '••••••••'
        })
    )

    class Meta:
        model = CustomUser
        fields = ('phone_number', 'first_name', 'last_name')
        widgets = {
            'phone_number': forms.TextInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-walnut-800 focus:ring-walnut-800 sm:text-lg p-3 dark:bg-slate-800 dark:border-slate-600',
                'placeholder': '09123456789'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-walnut-800 focus:ring-walnut-800 sm:text-lg p-3 dark:bg-slate-800 dark:border-slate-600',
                'placeholder': 'نام'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-walnut-800 focus:ring-walnut-800 sm:text-lg p-3 dark:bg-slate-800 dark:border-slate-600',
                'placeholder': 'نام خانوادگی'
            }),
        }

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if CustomUser.objects.filter(phone_number=phone_number).exists():
            raise forms.ValidationError("این شماره تلفن قبلا ثبت شده است.")
        return phone_number

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("کلمات عبور با یکدیگر مطابقت ندارند.")
        return confirm_password

class UserLoginForm(forms.Form):
    phone_number = forms.CharField(
        label='شماره تلفن',
        widget=forms.TextInput(attrs={
            'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-walnut-800 focus:ring-walnut-800 sm:text-lg p-3 dark:bg-slate-800 dark:border-slate-600',
            'placeholder': '09123456789'
        })
    )
    password = forms.CharField(
        label='کلمه عبور',
        widget=forms.PasswordInput(attrs={
            'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-walnut-800 focus:ring-walnut-800 sm:text-lg p-3 dark:bg-slate-800 dark:border-slate-600',
            'placeholder': '••••••••'
        })
    )

class OTPVerifyForm(forms.Form):
    code = forms.CharField(label='کد تایید', max_length=6, widget=forms.TextInput(attrs={
        'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-walnut-800 focus:ring-walnut-800 sm:text-lg p-3 text-center tracking-[1em] dark:bg-slate-800 dark:border-slate-600',
        'placeholder': '------'
    }))

class ForgotPasswordForm(forms.Form):
    phone_number = forms.CharField(label='شماره تلفن', widget=forms.TextInput(attrs={
        'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-walnut-800 focus:ring-walnut-800 sm:text-lg p-3 dark:bg-slate-800 dark:border-slate-600',
        'placeholder': 'شماره تلفنی که با آن ثبت نام کرده‌اید'
    }))

class SetNewPasswordForm(forms.Form):
    password = forms.CharField(label='کلمه عبور جدید', widget=forms.PasswordInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-walnut-800 focus:ring-walnut-800 sm:text-lg p-3 dark:bg-slate-800 dark:border-slate-600'}))
    confirm_password = forms.CharField(label='تکرار کلمه عبور جدید', widget=forms.PasswordInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-walnut-800 focus:ring-walnut-800 sm:text-lg p-3 dark:bg-slate-800 dark:border-slate-600'}))

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("کلمات عبور با یکدیگر مطابقت ندارند.")
        return confirm_password

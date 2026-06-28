import random
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from .forms import (
    UserRegistrationForm, UserLoginForm, OTPVerifyForm, ForgotPasswordForm, 
    SetNewPasswordForm, ProfileInfoForm, AddressForm
)
from .models import CustomUser, OTP, Address
from orders.models import Order

def generate_otp(user):
    code = str(random.randint(100000, 999999))
    OTP.objects.create(user=user, code=code)
    print(f"--- MOCK SMS: Your OTP for {user.phone_number} is: {code} ---")
    return code

def user_register(request):
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.is_phone_verified = False
            user.save()
            generate_otp(user)
            request.session['phone_number_for_otp'] = user.phone_number
            messages.success(request, 'ثبت نام موفق بود. کد تایید به شماره شما ارسال شد.')
            return redirect('accounts:otp_verify')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/login_register.html', {'form': form, 'page_type': 'register'})

def otp_verify(request):
    phone_number = request.session.get('phone_number_for_otp')
    if not phone_number:
        messages.error(request, 'شماره تلفن یافت نشد. لطفا مجددا تلاش کنید.')
        return redirect('accounts:register')

    user = get_object_or_404(CustomUser, phone_number=phone_number)
    if request.method == 'POST':
        form = OTPVerifyForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            two_minutes_ago = timezone.now() - timedelta(minutes=2)
            try:
                otp = OTP.objects.get(user=user, code=code, is_used=False, created_at__gte=two_minutes_ago)
                user.is_phone_verified = True
                user.save()
                otp.is_used = True
                otp.save()
                login(request, user)
                del request.session['phone_number_for_otp']
                messages.success(request, 'حساب شما با موفقیت فعال شد.')
                return redirect('accounts:dashboard')
            except OTP.DoesNotExist:
                messages.error(request, 'کد وارد شده نامعتبر یا منقضی شده است.')
    else:
        form = OTPVerifyForm()
    return render(request, 'accounts/otp_verify.html', {'form': form})

def user_login(request):
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, phone_number=cd['phone_number'], password=cd['password'])
            if user is not None:
                if not user.is_phone_verified:
                    generate_otp(user)
                    request.session['phone_number_for_otp'] = user.phone_number
                    messages.error(request, 'حساب شما فعال نشده است. لطفا کد تایید را وارد کنید.')
                    return redirect('accounts:otp_verify')
                login(request, user)
                messages.success(request, 'شما با موفقیت وارد شدید.')
                return redirect('accounts:dashboard')
            else:
                messages.error(request, 'شماره تلفن یا کلمه عبور نامعتبر است.')
    else:
        form = UserLoginForm()
    return render(request, 'accounts/login_register.html', {'form': form, 'page_type': 'login'})

@login_required
def user_logout(request):
    logout(request)
    messages.info(request, 'شما با موفقیت خارج شدید.')
    return redirect('shop:product_list')

@login_required
def user_dashboard(request):
    user = request.user
    profile_form = ProfileInfoForm(instance=user)
    address_form = AddressForm()
    
    if request.method == 'POST':
        if 'update_profile' in request.POST:
            profile_form = ProfileInfoForm(request.POST, instance=user)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, 'اطلاعات حساب شما با موفقیت به روز شد.')
                return redirect('accounts:dashboard')

        elif 'add_address' in request.POST:
            address_form = AddressForm(request.POST)
            if address_form.is_valid():
                address = address_form.save(commit=False)
                address.user = user
                address.save()
                messages.success(request, 'آدرس جدید با موفقیت اضافه شد.')
                return redirect('accounts:dashboard')
    
    orders = Order.objects.filter(user=user).order_by('-created_at')
    addresses = Address.objects.filter(user=user)

    context = {
        'orders': orders,
        'addresses': addresses,
        'profile_form': profile_form,
        'address_form': address_form,
        'section': request.GET.get('section', 'orders')
    }
    return render(request, 'accounts/dashboard.html', context)

@login_required
def set_default_address(request, pk):
    address = get_object_or_404(Address, pk=pk, user=request.user)
    address.is_default = True
    address.save()
    messages.success(request, 'آدرس پیش فرض با موفقیت تغییر کرد.')
    return redirect('accounts:dashboard')

def forgot_password(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            try:
                user = CustomUser.objects.get(phone_number=phone_number)
                generate_otp(user)
                request.session['phone_for_reset'] = phone_number
                messages.success(request, 'کد بازیابی برای شما ارسال شد.')
                return redirect('accounts:reset_verify_otp')
            except CustomUser.DoesNotExist:
                messages.error(request, 'کاربری با این شماره تلفن یافت نشد.')
    else:
        form = ForgotPasswordForm()
    return render(request, 'accounts/forgot_password.html', {'form': form})

def reset_verify_otp(request):
    phone_number = request.session.get('phone_for_reset')
    if not phone_number:
        return redirect('accounts:forgot_password')

    if request.method == 'POST':
        form = OTPVerifyForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            two_minutes_ago = timezone.now() - timedelta(minutes=2)
            user = CustomUser.objects.get(phone_number=phone_number)
            try:
                otp = OTP.objects.get(user=user, code=code, is_used=False, created_at__gte=two_minutes_ago)
                otp.is_used = True
                otp.save()
                request.session['otp_verified_for_reset'] = True
                messages.success(request, 'کد تایید شد. اکنون میتوانید رمز جدید را وارد کنید.')
                return redirect('accounts:set_new_password')
            except OTP.DoesNotExist:
                messages.error(request, 'کد وارد شده نامعتبر یا منقضی شده است.')
    else:
        form = OTPVerifyForm()
    return render(request, 'accounts/otp_verify.html', {'form': form, 'page_type': 'reset'})

def set_new_password(request):
    if not request.session.get('otp_verified_for_reset'):
        messages.error(request, 'ابتدا باید کد تایید را وارد کنید.')
        return redirect('accounts:forgot_password')

    phone_number = request.session.get('phone_for_reset')
    user = CustomUser.objects.get(phone_number=phone_number)

    if request.method == 'POST':
        form = SetNewPasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['password']
            user.set_password(new_password)
            user.save()
            
            del request.session['phone_for_reset']
            del request.session['otp_verified_for_reset']
            
            messages.success(request, 'رمز عبور شما با موفقیت تغییر کرد. لطفا وارد شوید.')
            return redirect('accounts:login')
    else:
        form = SetNewPasswordForm()
    return render(request, 'accounts/set_new_password.html', {'form': form})

from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.user_register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.user_dashboard, name='dashboard'),
    path('otp-verify/', views.otp_verify, name='otp_verify'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('reset-verify-otp/', views.reset_verify_otp, name='reset_verify_otp'),
    path('set-new-password/', views.set_new_password, name='set_new_password'),
]

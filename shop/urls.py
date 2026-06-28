from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.home_page, name='home_page'),
    path('shop/', views.product_list, name='product_list'),
    path('product/<str:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
]

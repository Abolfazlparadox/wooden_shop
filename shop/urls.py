# shop/urls.py

from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.home_page, name='home_page'),
    path('shop/', views.product_list, name='product_list'),
    path('shop/category/<str:category_slug>/', views.product_list, name='product_list_by_category'), # Corrected path converter
    path('product/<str:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('api/search-suggestions/', views.search_suggestions_api, name='search_suggestions_api'),
]

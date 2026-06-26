from django.urls import path
from .views import ProductListView, ProductDetailView

app_name = 'shop'

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('<str:slug>/', ProductDetailView.as_view(), name='product_detail'),
]

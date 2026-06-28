# blog/urls.py

from django.urls import path
from . import views # Assuming you will create views later

app_name = 'blog'

urlpatterns = [
    # path('', views.post_list, name='post_list'),
    # path('<slug:slug>/', views.post_detail, name='post_detail'),
]
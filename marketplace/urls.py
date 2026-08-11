from django.urls import path
from . import views

urlpatterns = [
    path('', views.marketplace_list, name='marketplace_list'),
    path('<int:pk>/', views.product_detail, name='product_detail'),
    path('sell/', views.product_create, name='product_create'),
]

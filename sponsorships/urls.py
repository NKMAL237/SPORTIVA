from django.urls import path
from . import views

urlpatterns = [
    path('', views.sponsorships_list, name='sponsorships_list'),
    path('create/', views.campaign_create, name='campaign_create'),
    path('<int:pk>/', views.campaign_detail, name='campaign_detail'),
]

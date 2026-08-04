from django.urls import path
from . import views

urlpatterns = [
    path('', views.sponsorships_list, name='sponsorships_list'),
]

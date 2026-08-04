from django.urls import path
from . import views

urlpatterns = [
    path('', views.media_feed_list, name='media_feed_list'),
]

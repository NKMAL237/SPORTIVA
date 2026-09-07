from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('offline/', views.offline_view, name='offline'),
    path('sw.js', views.service_worker, name='service_worker'),
    path('manifest.json', views.manifest, name='manifest'),
    path('api/sports-news/', views.sports_news_api, name='sports_news_api'),
]


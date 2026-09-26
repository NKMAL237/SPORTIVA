from django.urls import path
from . import views

urlpatterns = [
    path('', views.media_feed_list, name='media_feed_list'),
    path('create/', views.post_create, name='post_create'),
    path('<int:pk>/', views.post_detail, name='post_detail'),
    path('<int:pk>/like/', views.post_like, name='post_like'),
    path('<int:pk>/delete/', views.post_delete, name='post_delete'),
    path('comments/<int:pk>/delete/', views.comment_delete, name='comment_delete'),
]

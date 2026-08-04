from django.urls import path
from . import views

urlpatterns = [
    path('', views.organizations_list, name='organizations_list'),
    path('<int:pk>/', views.organization_detail, name='organization_detail'),
    path('create/', views.organization_create, name='organization_create'),
]

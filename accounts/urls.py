from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.profile_edit_view, name='profile_edit'),
    path('profile/<str:username>/', views.user_detail_view, name='user_detail'),
    path('profile/<str:username>/view/', views.user_detail_view, name='profile_detail'),
    path('profiles/', views.profiles_list_view, name='profiles_list'),
    path('follow/<int:user_id>/', views.toggle_follow_view, name='toggle_follow'),
    path('exploits/add/', views.add_exploit_view, name='add_exploit'),
    path('exploits/<int:exploit_id>/edit/', views.edit_exploit_view, name='edit_exploit'),
    path('exploits/<int:exploit_id>/delete/', views.delete_exploit_view, name='delete_exploit'),
    path('exploits/<int:exploit_id>/verify/', views.verify_exploit_view, name='verify_exploit'),
    path('athletes/<int:athlete_id>/endorse/', views.endorse_athlete_view, name='endorse_athlete'),
    path('athletes/<int:athlete_id>/unendorse/', views.remove_endorsement_view, name='remove_endorsement'),
    path('users/', views.user_management_view, name='user_management'),
    path('users/<int:user_id>/update-tabs/', views.user_update_tabs_view, name='user_update_tabs'),
]

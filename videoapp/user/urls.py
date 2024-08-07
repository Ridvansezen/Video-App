from django.urls import path
from user import views
from django.contrib.auth import views as auth_views

app_name = 'user'

urlpatterns = [
    path('register/', views.register_user, name='register_user'),
    path('login/', views.login_user, name='login_user'),
    path('logout/', views.logout_user, name='logout_user'),
    path('profile/', views.request_user_profile, name='request_profile_user'),
    path('profile/<int:user_id>/', views.view_profile, name='view_profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('<int:user_id>/password/', views.change_password, name='change_password'),
]
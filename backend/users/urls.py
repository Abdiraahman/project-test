# users/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.UserRegistrationView.as_view(), name='user-register'),
    path('login/', views.login_view, name='user-login'),
    path('profile-status/', views.profile_status_view, name='profile-status'),
    path('create_company/', views.CompanyRegistrationView.as_view(), name='create-company'),
    path('profile-view/', views.profile_view, name='profile-view'),
    path('logout/', views.logout_view, name='user-logout'),
    path('refresh/', views.refresh_token_view, name='refresh-token'),
]

from django.contrib.auth import views as django_views
from django.contrib import admin
from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('test/', views.test, name='test'),

    path('register/', views.RegisterAuthView.as_view(), name='register'),
    path('login/', django_views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutAuthView.as_view(), name='logout'),

    path('change_password/', views.ChangePasswordAuthView.as_view(), name='change_password'),
    path('change_password_done/', views.ChangePasswordDoneView.as_view(), name='change_password_done'),

    # if you wanna use reset password option so should set SMTP configuration on settings.py
    path('reset_password/', django_views.PasswordResetView.as_view( 
        template_name='registration/reset_password.html'), name='reset_password'),
    path('reset_password_sent/', django_views.PasswordChangeDoneView.as_view(
        template_name='registration/reset_password_sent.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', django_views.PasswordResetConfirmView.as_view(
        template_name='registration/reset_password_confirm.html'), name='password_reset_confirm'),
    path('reset_password_complete/', django_views.PasswordResetCompleteView.as_view(
        template_name='registration/reset_password_complete.html'), name='password_reset_complete'),
]
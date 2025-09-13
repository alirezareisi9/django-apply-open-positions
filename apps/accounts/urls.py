from django.contrib.auth import views as django_views
from django.contrib import admin
from django.urls import path
from . import views

app_name = "accounts"
urlpatterns = [
    path("", views.test, name="test"),
    path(
        "register/",
        views.RegisterView.as_view(template_name="registration/register.html"),
        name="register",
    ),
    path(
        "register/verification/<uuid:uid>/",
        views.RegisterVerificationView.as_view(
            template_name="registration/register_verification.html"
        ),
        name="register-verification",
    ),
    path(
        "login/",
        views.LoginView.as_view(template_name="registration/login.html"),
        name="login",
    ),
    path(
        "logout/",
        views.LogoutView.as_view(),
        name="logout",
    ),
    path(
        "update-profile/",
        views.UpdateProfileView.as_view(
            template_name="registration/update_profile.html"
        ),
        name="update-profile",
    ),
    path(
        "change-password/",
        views.ChangePasswordView.as_view(
            template_name="registration/change_password.html"
        ),
        name="change-password",
    ),
    path(
        "change-password-done/",
        views.ChangePasswordDoneView.as_view(),
        name="change-password-done",
    ),
    path(
        "reset-password/",
        views.ResetPasswordView.as_view(
            template_name="registration/reset_password.html"
        ),
        name="reset-password",
    ),
    path(
        "reset-password-sent/",
        views.ResetPasswordSentView.as_view(),
        name="reset-password-sent",
    ),
    path(
        "reset-password/<uuid:uid>/",
        views.ResetPasswordConfirmView.as_view(
            template_name="registration/reset_password_confirm.html"
        ),
        name="reset-password-confirm",
    ),
    path(
        "reset-password-complete/",
        views.ResetPasswordCompleteView.as_view(),
        name="reset-password-complete",
    ),
]
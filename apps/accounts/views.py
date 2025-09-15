import random
from django.contrib import messages
from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.forms import (
    PasswordChangeForm,
    AuthenticationForm,
    SetPasswordForm,
)
from django.contrib.auth.views import LoginView as DjangoLoginView, PasswordChangeView
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect, HttpResponse
from django.views.generic import CreateView, UpdateView, FormView, View
from django.urls import reverse_lazy
from django.http import response
from django.core.mail import EmailMessage
from django.core.validators import validate_email
from . import forms
from . import models


def test(request):
    return HttpResponse("Hello Successful Man!")


class RegisterView(CreateView):
    form_class = forms.RegisterForm
    object_uid = None

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)  # super return kwargs

        if "form" not in kwargs:
            kwargs["form"] = self.get_form()
        return kwargs

    def form_valid(self, form):
        user = form.save(commit=False)
        code = random.randint(100000, 999999)
        user.verification_code = code

        validate_email(user.email)

        user.is_active = False
        user.set_password(user.password)
        user.save()

        self.object_uid = user.uid

        email = EmailMessage(
            subject="Apply Registration Verification Code",
            body=f"Verification Code : {user.verification_code}",
            from_email="verification<volleyalireza@gmail.com>",
            to=[user.email],
        )
        
        email.send(fail_silently=False)

        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse_lazy(
            "accounts:register-verification", kwargs={"uid": self.object_uid}
        )


class RegisterVerificationView(FormView):
    form_class = forms.RegisterVerificationForm
    model = models.CustomUser

    def get_object(self):
        uid = self.kwargs.get("uid")
        user = get_object_or_404(self.model, uid=uid)
        return user

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        kwargs["user"] = self.get_object()

        return kwargs

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)

        if "form" not in kwargs:
            kwargs["form"] = self.get_form()

        return kwargs

    def form_valid(self, form):
        user = self.get_object()

        user.regenerate_uuid()

        user.is_active = True
        user.save()

        login(self.request, user)

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("accounts:test")


class LoginView(FormView):
    form_class = forms.LoginForm
    template_name = "registration/login.html"

    def form_valid(self, form):
        login(self.request, form.user)

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("accounts:test")


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(self.request)

        return redirect("accounts:test")


class UpdateProfileView(UpdateView):
    form_class = forms.UpdateProfileForm

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy("accounts:test")


class ChangePasswordView(PasswordChangeView):
    success_url = reverse_lazy("accounts:change-password-done")


class ChangePasswordDoneView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "registration/change_password_done.html")


class ResetPasswordView(FormView):
    form_class = forms.ResetPasswordForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if "form" not in context:
            context["form"] = self.get_form()
        return context

    def form_valid(self, form):
        email = form.cleaned_data.get("email")

        User = get_user_model()
        user = get_object_or_404(User, email=email)

        url = self.request.build_absolute_uri(f"{user.uid}/")

        email = EmailMessage(
            subject="Apply Registration Update Password",
            body=f"Click here to update password : {url}",
            from_email="Reset Password Verification<volleyalireza@gmail.com>",
            to=[user.email],
        )

        email.send(fail_silently=False)

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("accounts:reset-password-sent")


class ResetPasswordSentView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "registration/reset_password_sent.html")


class ResetPasswordConfirmView(FormView):
    form_class = SetPasswordForm

    def get_object(self):
        uid = self.kwargs.get("uid")
        User = get_user_model()
        return get_object_or_404(User, uid=uid)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.get_object()
        return kwargs

    def form_valid(self, form):
        password = form.cleaned_data.get("new_password1")

        user = self.get_object()

        validate_password(password, user)

        user.set_password(password)
        user.regenerate_uuid()

        user.is_active = True
        user.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("accounts:reset-password-complete")


class ResetPasswordCompleteView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "registration/reset_password_complete.html")

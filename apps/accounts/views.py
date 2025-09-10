import random
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.forms import PasswordChangeForm, AuthenticationForm
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.shortcuts import render, redirect, HttpResponse
from django.views.generic import CreateView, View
from django.urls import reverse_lazy
from django.http import response
from django.core.mail import EmailMessage
from . import forms
from . import models


class RegisterView(CreateView):
    form_class = forms.RegisterForm

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)  # super return kwargs

        if "form" not in kwargs:
            kwargs["form"] = self.get_form()
        return kwargs

    def form_valid(self, form):
        
        user = form.save(commit=False)
        code = random.randint(100000, 999999)
        user.verification_code = code
        
        user.set_password(user.password)
        user.save()

        email = EmailMessage(
            subject='Hima Registration Verification Code',
            body=f'Verification Code : {user.verification_code}',
            from_email='verification<hima.sport.org@gmail.com>',
            to=[user.email]
        )

        email.send(fail_silently=False)
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse_lazy("accounts:login")




class LoginAuthView(LoginView):
    form_class = AuthenticationForm
    template_name = "registration/login.html"

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)

        if "form" not in kwargs:
            kwargs["form"] = self.get_form()
        return kwargs

    def form_valid(self, form: AuthenticationForm) -> HttpResponse:
        response = super().form_valid(form)

        messages.success(self.request, f"Welcome {self.request.user}!")
        return response

    def get_success_url(self) -> str:
        return reverse_lazy("/")


class LogoutAuthView(View):
    def get(self, request, *args, **kwargs):
        logout(self.request)

        messages.success(self.request, "successfully logout!")
        return redirect("accounts:login")


class ChangePasswordAuthView(PasswordChangeView):
    template_name = "registration/change_password.html"
    success_url = reverse_lazy("accounts:change_password_done")


class ChangePasswordDoneView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "registration/change_password_done.html")

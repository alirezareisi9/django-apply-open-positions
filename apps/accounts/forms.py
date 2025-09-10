from django.contrib.auth.forms import UserCreationForm
from django import forms
from . import models


class RegisterForm(UserCreationForm):
    class Meta:
        model = models.CustomUser
        fields = [
            "email",
        ]


class LoginForm(forms.ModelForm):
    class Meta:
        model = models.CustomUser
        fields = ["email", "password"]

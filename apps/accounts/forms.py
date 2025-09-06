from django.contrib.auth.forms import UserCreationForm
from django import forms
from . import models

class RegisterForm(UserCreationForm):
    class Meta:
        model = models.CustomUser
        fields = ['email', 'first_name','last_name', 'major', 'field',]
    

class LoginForm(forms.ModelForm):
    class Meta:
        model = models.CustomUser
        fields = ['email', 'password']
 
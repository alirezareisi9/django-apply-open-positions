from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django import forms
from . import models


class RegisterForm(UserCreationForm):
    class Meta:
        model = models.CustomUser
        fields = [
            "email",
        ]


class RegisterVerificationForm(forms.Form):
    error_css_class = "error"
    error_messages = {"incorrect": _("Your Code isn't correct")}

    verification_code = forms.CharField(
        widget=forms.TextInput(attrs={"size": 6, "required": True})
    )

    def __init__(self, user=None, *args, **kwargs):
        super(RegisterVerificationForm, self).__init__(*args, **kwargs)

        self.user = user

    def clean(self):
        cleaned_data = super(RegisterVerificationForm, self).clean()
        code = cleaned_data.get("verification_code")
        if code != self.user.verification_code:
            raise ValidationError(
                self.error_messages.get("incorrect"), code=self.error_css_class
            )

        return cleaned_data


class LoginForm(forms.ModelForm):
    class Meta:
        model = models.CustomUser
        fields = ["email", "password"]

from django.contrib.auth.forms import UserCreationForm

from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.core.validators import validate_email
from . import models


class RegisterForm(UserCreationForm):
    class Meta:
        model = models.CustomUser
        fields = [
            "email",
        ]

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")

        if validate_email(email):
            User = get_user_model()
            user = User.objects.filter(email=email).first()

            if not user:
                raise ValidationError(
                    self.error_messages.get("not_exist"), code="not_exist"
                )

            return email


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
                self.error_messages.get("incorrect"), code="incorrect"
            )

        return cleaned_data


class LoginForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput(attrs={"required": True}))

    error_messages = {
        "invalid_login": _("Please enter a correct email and password."),
        "inactive": _("This account is inactive."),
    }

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        if email and password:
            user = authenticate(email=email, password=password)
            if user is None:
                raise ValidationError(
                    self.error_messages["invalid_login"], code="invalid_login"
                )
            if not user.is_active:
                raise ValidationError(self.error_messages["inactive"], code="inactive")

            self.user = user

        return cleaned_data


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = models.CustomUser
        fields = ["email", "first_name", "last_name", "major", "field"]

        widgets = {
            "email": forms.EmailInput(attrs={"readonly": "readonly"}),
        }


class ResetPasswordForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={"required": True}))

    error_messages = {
        "not_exist": _("No user with this email exist"),
    }

    def clean_email(self):
        email = self.cleaned_data.get("email")

        validate_email(email)
        User = get_user_model()
        user = User.objects.filter(email=email).first()

        if not user:
            raise ValidationError(
                self.error_messages.get("not_exist"), code="not_exist"
            )

        return email

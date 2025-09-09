from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from . import models


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = models.CustomUser
        fields = ('first_name', 'last_name', 'email', \
                    'is_active', \
                        'is_staff', 'is_superuser')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = models.CustomUser
        fields = ('first_name', 'last_name', 'phone_number', 'national_code', \
                  'employee_code', 'role', 'manager', 'change_password', \
                    'leave_limit', 'is_active', \
                        'is_staff', 'is_superuser')

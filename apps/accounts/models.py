from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models
from . import managers



class CustomUser(AbstractUser, PermissionsMixin):
    # 'username, password, email, first_name, last_name, password, last_login, is_active, is_staff' on django AbstractBaseUser
    username=None
    email = models.EmailField(unique=True)
    major = models.CharField(max_length=150)
    field = models.CharField(max_length=150)
    last_login = None
    
    # Field that user cannot fill : is_active, is_superuser

    objects = managers.CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password']

    def __str__(self) -> str:
        return self.email
    

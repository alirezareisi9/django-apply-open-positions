from django.contrib.auth.models import AbstractUser
from django.db import models
from . import managers



class CustomUser(AbstractUser):
    # 'username, password, email, first_name, last_name, password,
    #  last_login, date_joined, is_active, is_staff' on django AbstractUser
    
    # 'is_superuser, group' permissions methods
    #  and fields needed on django PermissionsMixin
    
    username=None
    email = models.EmailField(unique=True)
    major = models.CharField(max_length=150)
    field = models.CharField(max_length=150)
    last_login = None
    
    # Field that user cannot fill :
    # 'date_joined, is_active, is_staff, is_superuser'

    objects = managers.CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = None

    def __str__(self) -> str:
        return self.email
    

import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from . import managers
from apps.edu.models import Major, Field


class CustomUser(AbstractUser):
    # 'username, password, email, first_name, last_name,
    #  last_login, date_joined, is_active, is_staff' on django AbstractUser

    # 'is_superuser, group' permissions methods
    #  and fields needed on django PermissionsMixin
    uid = models.UUIDField(default=uuid.uuid4, unique=True)

    email = models.EmailField(unique=True)
    major = models.ForeignKey(
        Major, on_delete=models.PROTECT, blank=True, null=True, related_name="users"
    )
    field = models.ForeignKey(
        Field, on_delete=models.PROTECT, blank=True, null=True, related_name="users"
    )
    verification_code = models.CharField(max_length=6, blank=True, null=True)

    last_login = None
    username = None

    # Field that user cannot access :
    # 'date_joined, is_active, is_staff, is_superuser'

    objects = managers.CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self) -> str:
        return self.email

    def regenerate_uuid(self):
        while True:
            new_uid = uuid.uuid4()
            if not CustomUser.objects.filter(uid=new_uid).exists():
                self.uid = new_uid
                self.save()
                break

from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


class CustomUserManager(BaseUserManager):
    use_in_migrations = True  # True by default on BaseUserManager
    # Set it False -> use default django manager model in migrations
    #  which break your instance creation logic

    def _create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_("Fill out email field!"))

        if self.model.REQUIRED_FIELDS:
            required = iter(self.model.REQUIRED_FIELDS)

            for field in required:
                if not extra_fields.get(field):
                    raise ValueError(_("Fill out {} fields!", format=field))

        # Just normalize email and don't validating it
        email = self.normalize_email(email)
        # "weird@local@domain.com".rsplit("@", 1)  :
        #  rightsplit(separator, maxsplit)
        # → ["weird@local", "domain.com"]

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        # Without using=self._db:
        # user.save() would default to the "default" database.
        # But if your manager/queryset came from a non-default database,
        # the object might accidentally be saved
        #  to the wrong database(default db)

        return user

    def create_user(self, email, password, **extra_fields):
        extra_fields.setdefault("is_active", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_staff", False)

        return self._create_user(email=email, password=password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)

        return self._create_user(email=email, password=password, **extra_fields)

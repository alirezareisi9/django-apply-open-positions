from django.contrib.auth.base_user import BaseUserManager
from . import models


class CustomUserManager(BaseUserManager):

    use_in_migrations = True

    def _create_user(self, email, password=None, **extra_fields):
        required_register_fields = self.model.REQUIRED_FIELDS
        email_value = self.model.USERNAME_FIELD

        if not email_value:
                raise ValueError('Fill out required fields!')

        for field in required_register_fields:
            if not field:
                raise ValueError('Fill out required fields!')
        
        
        email = self.normalize_email(email)

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user
    


    def create_user(self, email, password, **extra_fields):

        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_staff', False)

        return self._create_user(email=email, password=password, **extra_fields)
    

    
    def create_superuser(self, email, password, **extra_fields):

        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        return self._create_user(email=email, password=password, **extra_fields)

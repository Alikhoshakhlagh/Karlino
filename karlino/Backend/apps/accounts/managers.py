from django.contrib.auth.models import BaseUserManager
from ..core.messages import *


class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None, **extra_fields):
        if not email:
            raise ValueError(
                EMAIL_REQUIRED
            )

        if not first_name:
            raise ValueError(
                FIRST_NAME_REQUIRED
            )

        if not last_name:
            raise ValueError(
                LAST_NAME_REQUIRED
            )

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, first_name, last_name, password, **extra_fields)
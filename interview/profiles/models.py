from django.db import models
from django.contrib.auth.models import AbstractUser
from typing import Optional

from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(
        self, phone: str,
        password: Optional[str],
        **extra_fields
    ):
        """
        Create and save a user with the given email, and password.
        """
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password) if password else user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_user(
            self,
            email: str,
            password: str = None,
            **extra_fields
    ):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(
            self,
            email: str,
            password: str,
            **extra_fields
    ):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        user = self.model(email=email, **extra_fields)
        user.set_password(password) if password else user.set_unusable_password()
        user.save(using=self._db)
        return user


class UserProfile(AbstractUser):

    # overwritten to remove the useless `username` field from database
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    username = None
    avatar = models.ImageField("Avatar", upload_to="avatars")
    email = models.EmailField("email address", unique=True)
    objects: UserManager = UserManager()  # type: ignore

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"

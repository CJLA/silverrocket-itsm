import uuid

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class CustomUserManager(BaseUserManager):
    """
    User manager that authenticates with email instead of username.
    """

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email field must be set")

        email = self.normalize_email(email)

        user = self.model(email=email, **extra_fields)

        user.set_password(password)

        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("role", CustomUser.Roles.ADMIN)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    """User model that authenticates with email instead of username."""

    username = None

    class Roles(models.TextChoices):
        """Application roles used by SilverRocket authorization logic."""

        ADMIN = "ADMIN", "Administrator"
        MANAGER = "MANAGER", "Manager"
        TECHNICIAN = "TECHNICIAN", "Technician"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    email = models.EmailField(unique=True)

    role = models.CharField(
        max_length=20,
        choices=Roles.choices,
        default=Roles.TECHNICIAN,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

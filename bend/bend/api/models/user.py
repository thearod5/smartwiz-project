import uuid

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """Create and return a regular user."""
        if not email:
            raise ValueError('The Email field must be set.')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and return a superuser."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not extra_fields.get('is_staff'):
            raise ValueError('Superuser must have is_staff=True.')
        if not extra_fields.get('is_superuser'):
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    objects = CustomUserManager()  # Use the custom manager
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # Keeps your UUID primary key
    email = models.EmailField(unique=True)  # Ensure email is unique
    middle_name = models.CharField(max_length=150, null=True, blank=True)  # Optional field
    primary_address = models.ForeignKey(
        "api.Address",
        on_delete=models.SET_NULL,
        related_name='primary_users',
        null=True,
        blank=True,
        help_text="The user's primary address, if specified."
    )

    username = None  # Remove the username field
    USERNAME_FIELD = 'email'  # Set email as the unique identifier
    REQUIRED_FIELDS = ['first_name', 'last_name']  # Fields required when creating a superuser

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        ordering = ['first_name', 'last_name']

import uuid

from django.db import models

from app.models.constants import MEDIUM_LEN, SHORT_LEN


class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # Uniquely identifies the user
    name = models.CharField(max_length=SHORT_LEN)
    password = models.CharField(max_length=MEDIUM_LEN)
    email = models.EmailField(unique=True)  # Ensures no duplicate emails
    primary_address = models.ForeignKey(
        "app.Address",
        on_delete=models.SET_NULL,
        related_name='primary_users',
        null=True,
        blank=True,
        help_text="The user's primary address, if specified."
    )
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set to the current timestamp when created
    updated_at = models.DateTimeField(auto_now=True)  # Automatically updated on save

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']  # Orders querysets alphabetically by name

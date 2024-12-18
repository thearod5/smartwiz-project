import uuid

from django.db import models

from api.models.constants import LONG_LEN, MEDIUM_LEN


class Address(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # Uniquely identifies the user
    user = models.ForeignKey(
        "api.User",
        on_delete=models.CASCADE,
        related_name="addresses",
        help_text="The user associated with this address."
    )
    display = models.CharField(max_length=LONG_LEN, help_text="A user-friendly representation of the address.")
    street = models.CharField(max_length=MEDIUM_LEN)
    city = models.CharField(max_length=MEDIUM_LEN)
    state = models.CharField(max_length=MEDIUM_LEN)
    zip_code = models.CharField(max_length=MEDIUM_LEN)
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set when created
    updated_at = models.DateTimeField(auto_now=True)  # Automatically set on update

    class Meta:
        ordering = ['city', 'state']  # Default ordering for querysets
        verbose_name = "Address"
        verbose_name_plural = "Addresses"

    def __str__(self):
        return f"{self.display} ({self.city}, {self.state})"

import uuid

from django.db import models


class Return(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey("api.User", on_delete=models.CASCADE, related_name='returns')
    year = models.PositiveIntegerField()
    annual_income = models.FloatField(null=True, blank=True)
    attended_school = models.BooleanField(null=True, blank=True)
    owned_home = models.BooleanField(null=True, blank=True)
    # Calculated fields
    taxable_income = models.FloatField(null=True, blank=True)
    taxes_owed = models.FloatField(null=True, blank=True)
    taxes_refunded = models.FloatField(null=True, blank=True)
    # Automatic fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'year')  # A user should only have one return per year

    def __str__(self):
        return f"{str(self.user)} - {self.year} Return"

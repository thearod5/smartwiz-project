import uuid

from django.db import models

from api.models import Return


class Item(models.Model):
    DEDUCTION = "deduction"
    CREDIT = "credit"
    TYPE_CHOICES = [
        (DEDUCTION, "Deduction"),
        (CREDIT, "Credit"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    return_record = models.ForeignKey(
        Return,
        on_delete=models.CASCADE,
        related_name='items'
    )  # Many-to-one relationship with Return
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)  # Long description
    amount = models.FloatField()

    class Meta:
        verbose_name_plural = "Itemizations"

    def __str__(self):
        return f"{self.name} ({self.type}) - ${self.amount} for {self.year}"

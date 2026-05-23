from django.db import models
from apps.core.models import TimeStampedUUIDModel


class Company(TimeStampedUUIDModel):
    owner = models.OneToOneField(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name="company"
    )

    name = models.CharField(max_length=200, db_index=True)
    description = models.TextField(blank=True)
    website = models.URLField(blank=True, null=True)
    logo = models.URLField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=255, blank=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.name
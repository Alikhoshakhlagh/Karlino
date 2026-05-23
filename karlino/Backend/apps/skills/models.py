from django.db import models

from apps.core.models import TimeStampedUUIDModel


class Skill(TimeStampedUUIDModel):
    name = models.CharField(
        max_length=100,
        unique=True,
        db_index=True
    )

    slug = models.SlugField(
        unique=True,
        db_index=True
    )

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
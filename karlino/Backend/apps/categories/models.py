from django.db import models

from ..core.models import TimeStampedUUIDModel
from django.core.validators import RegexValidator


class Category(TimeStampedUUIDModel):
    name = models.CharField(
        max_length=100,
        unique=True,
        db_index=True
    )

    slug = models.SlugField(
        unique=True,

        validators=[
            RegexValidator(
                regex=r'^[a-z0-9-]+$',

                message=(
                    'Slug must contain only '
                    'english lowercase letters, '
                    'numbers, and hyphens.'
                ),
            )
        ]
    )

    icon = models.CharField(
        max_length=100,
        blank=True,
    )

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
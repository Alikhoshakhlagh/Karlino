from django.db import models

from apps.core.models import TimeStampedUUIDModel


class Favorite(TimeStampedUUIDModel):
    user = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='favorites'
    )

    project = models.ForeignKey(
        'projects.Project',
        on_delete=models.CASCADE,
        related_name='favorites'
    )

    class Meta:
        unique_together = ('user', 'project')

    def __str__(self):
        return f'{self.user} , {self.project}'
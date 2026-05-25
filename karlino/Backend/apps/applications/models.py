from django.db import models

from apps.core.models import TimeStampedUUIDModel


class Application(TimeStampedUUIDModel):

    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        ACCEPTED = 'accepted', 'Accepted'
        REJECTED = 'rejected', 'Rejected'
        WITHDRAWN = 'withdrawn', 'Withdrawn'

    project = models.ForeignKey(
        'projects.Project',
        on_delete=models.CASCADE,
        related_name='applications'
    )

    applicant = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='applications'
    )

    cover_letter = models.TextField()

    proposed_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        db_index=True
    )

    class Meta:
        unique_together = ('project', 'applicant')

    def __str__(self):
        return f'{self.applicant} -> {self.project}'
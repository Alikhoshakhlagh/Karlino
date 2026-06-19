from django.db import models

from .. import projects, accounts
from ..core.models import TimeStampedUUIDModel


class Bid(TimeStampedUUIDModel):

    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        SHORTLISTED = 'shortlisted', 'Shortlisted'
        ACCEPTED = 'accepted', 'Accepted'
        REJECTED = 'rejected', 'Rejected'
        WITHDRAWN = 'withdrawn', 'Withdrawn'

    project = models.ForeignKey(
        'projects.Project',
        on_delete=models.CASCADE,
        related_name='bids',
    )

    freelancer = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='bids',
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    delivery_days = models.PositiveIntegerField()

    cover_letter = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        db_index=True,
    )

    accepted_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    class Meta:

        constraints = [
            models.UniqueConstraint(
                fields=[
                    'project',
                    'freelancer',
                ],
                name='unique_bid_per_project',
            )
        ]

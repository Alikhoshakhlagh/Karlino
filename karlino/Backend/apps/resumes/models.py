from django.db import models

from .. import accounts
from ..core.models import TimeStampedUUIDModel


class Resume(TimeStampedUUIDModel):

    user = models.OneToOneField(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='resume',
    )

    headline = models.CharField(
        max_length=120,
    )

    about = models.TextField(
        blank=True,
        default='',
    )

    city = models.CharField(
        max_length=100,
        blank=True,
        default='',
    )

    website = models.URLField(
        blank=True,
        null=True,
    )

    github = models.URLField(
        blank=True,
        null=True,
    )

    skills = models.ManyToManyField(
        'skills.Skill',
        blank=True,
        related_name='resumes',
    )

    is_public = models.BooleanField(
        default=True,
        db_index=True,
    )

    def __str__(self):
        return f'{self.user.email} - {self.headline}'


class ResumeExperience(TimeStampedUUIDModel):

    resume = models.ForeignKey(
        Resume,
        on_delete=models.CASCADE,
        related_name='experiences',
    )

    title = models.CharField(
        max_length=120,
    )

    company = models.CharField(
        max_length=120,
        blank=True,
        default='',
    )

    description = models.TextField(
        blank=True,
        default='',
    )

    start_date = models.DateField()

    end_date = models.DateField(
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return f'{self.resume.user.email} - {self.title}'

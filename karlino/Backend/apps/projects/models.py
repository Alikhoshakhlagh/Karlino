from django.db import models

from apps.core.models import TimeStampedUUIDModel


class Project(TimeStampedUUIDModel):
    class OwnerType(models.TextChoices):
        PERSONAL = 'personal', 'Personal'
        COMPANY = 'company', 'Company'

    class Status(models.TextChoices):
        DRAFT = 'draft', 'Draft'
        ACTIVE = 'active', 'Active'
        CLOSED = 'closed', 'Closed'
        ARCHIVED = 'archived', 'Archived'

    creator = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='projects'
    )

    owner_type = models.CharField(
        max_length=20,
        choices=OwnerType.choices,
        default=OwnerType.PERSONAL,
        db_index=True,
    )

    company = models.ForeignKey(
        'companies.Company',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='projects'
    )

    primary_category = models.ForeignKey(
        'categories.Category',
        on_delete=models.PROTECT,
        related_name='primary_projects'
    )

    categories = models.ManyToManyField(
        'categories.Category',
        related_name='projects',
        blank=True,
    )

    title = models.CharField(
        max_length=200,
        db_index=True
    )

    description = models.TextField()

    budget_min = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )

    budget_max = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )

    location = models.CharField(
        max_length=120,
        blank=True,
        db_index=True
    )

    deadline = models.DateField(
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT,
        db_index=True
    )

    skills = models.ManyToManyField(
        'skills.Skill',
        related_name='projects',
        blank=True
    )

    def __str__(self):
        return self.title

    @property
    def display_owner_name(self):
        if self.owner_type == self.OwnerType.COMPANY and self.company:
            return self.company.name
        return f'{self.creator.first_name} {self.creator.last_name}'.strip()

    @property
    def is_company_project(self):
        return self.owner_type == self.OwnerType.COMPANY and self.company_id is not None
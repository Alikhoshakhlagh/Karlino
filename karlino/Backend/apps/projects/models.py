from django.db import models

from .. import accounts, companies, categories, skills, projects
from ..core.models import TimeStampedUUIDModel

class Project(TimeStampedUUIDModel):
    class OwnerType(models.TextChoices):
        PERSONAL = 'personal', 'Personal'
        COMPANY = 'company', 'Company'

    class Status(models.TextChoices):
        DRAFT = 'draft', 'Draft'
        ACTIVE = 'active', 'Active'
        CLOSED = 'closed', 'Closed'
        COMPLETED = 'completed', 'Completed'
        ARCHIVED = 'archived', 'Archived'

    class ProjectMode(models.TextChoices):
        SIMPLE = 'simple', 'Simple'
        TENDER = 'tender', 'Tender'

    class ReviewStatus(models.TextChoices):
        PENDING = 'pending', 'Pending'
        APPROVED = 'approved', 'Approved'
        REJECTED = 'rejected', 'Rejected'
        NEEDS_REVISION = 'needs_revision', 'Needs Revision'

    class SkillLevel(models.TextChoices):
        NONE = 'none', 'بدون نیاز به مهارت'
        BEGINNER = 'beginner', 'مبتدی'
        INTERMEDIATE = 'intermediate', 'متوسط'
        EXPERT = 'expert', 'حرفه‌ای'

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
        max_length=120,
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

    project_mode = models.CharField(
        max_length=20,
        choices=ProjectMode.choices,
        default=ProjectMode.SIMPLE,
        db_index=True
    )

    skill_level = models.CharField(
        max_length=20,
        choices=SkillLevel.choices,
        default=SkillLevel.NONE,
        db_index=True,
    )

    review_status = models.CharField(
        max_length=20,
        choices=ReviewStatus.choices,
        default=ReviewStatus.PENDING,
        db_index=True,
    )

    #Review
    reviewed_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviewed_projects',
    )

    reviewed_at = models.DateTimeField(
        null=True,
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


class ProjectReview(TimeStampedUUIDModel):

    class Status(models.TextChoices):
        APPROVED = 'approved', 'Approved'
        REJECTED = 'rejected', 'Rejected'
        NEEDS_REVISION = 'needs_revision', 'Needs Revision'


    project = models.ForeignKey(
        'projects.Project',
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    expert = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='project_reviews'
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
    )
    comment = models.TextField(
        blank=True,
        default='',
    )


class Milestone(TimeStampedUUIDModel):
    """
    Delivery stage of a project after a winner is picked.
    pending -> delivered (by the winner) -> approved (by the owner).
    """

    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        DELIVERED = 'delivered', 'Delivered'
        APPROVED = 'approved', 'Approved'

    project = models.ForeignKey(
        'projects.Project',
        on_delete=models.CASCADE,
        related_name='milestones',
    )

    title = models.CharField(
        max_length=120,
    )

    description = models.TextField(
        blank=True,
        default='',
    )

    due_date = models.DateField(
        null=True,
        blank=True,
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        db_index=True,
    )

    delivered_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    approved_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'{self.project.title} - {self.title}'

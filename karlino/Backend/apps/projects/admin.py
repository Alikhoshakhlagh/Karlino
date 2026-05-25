from django.contrib import admin

from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'creator',
        'owner_type',
        'primary_category',
        'status',
        'created_at',
    )

    search_fields = (
        'title',
        'description',
        'location',
    )

    list_filter = (
        'owner_type',
        'status',
        'primary_category',
    )

    filter_horizontal = (
        'categories',
        'skills',
    )
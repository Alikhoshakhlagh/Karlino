from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    ordering = ('email',)

    list_display = (
        'email',
        'first_name',
        'last_name',
        'gender',
        'is_staff',
        'is_active',
        'is_expert',
    )

    search_fields = (
        'email',
        'first_name',
        'last_name',
        'phone',
    )

    fieldsets = (
        (None, {
            'fields': (
                'email',
                'password',
            )
        }),

        ('Personal Info', {
            'fields': (
                'first_name',
                'last_name',
                'date_of_birth',
                'gender',
                'phone',
                'avatar',
            )
        }),

        ('Permissions', {
            'fields': (
                'is_active',
                'is_staff',
                'is_expert',
                'is_superuser',
                'groups',
                'user_permissions',
            )
        }),

        ('Dates', {
            'fields': (
                'last_login',
            )
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),

            'fields': (
                'email',
                'first_name',
                'last_name',
                'date_of_birth',
                'gender',
                'password1',
                'password2',
                'is_staff',
                'is_active',
                'is_expert',
            ),
        }),
    )

    filter_horizontal = (
        'groups',
        'user_permissions',
    )
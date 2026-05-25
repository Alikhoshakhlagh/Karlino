import re

from rest_framework import serializers

from .models import Category
from .constants import CATEGORY_ICONS


class CategorySerializer(serializers.ModelSerializer):

    resolved_icon = serializers.SerializerMethodField()

    class Meta:

        model = Category

        fields = (
            'id',
            'name',
            'slug',
            'icon',
            'resolved_icon',
        )

    def get_resolved_icon(self, obj):

        if obj.icon:
            return obj.icon

        return CATEGORY_ICONS.get(
            obj.slug,
            CATEGORY_ICONS['default'],
        )

    def validate_slug(self, value):
        if not re.match(r'^[a-z0-9-]+$', value):
            raise serializers.ValidationError(
                (
                    'Slug must contain only '
                    'english lowercase letters, '
                    'numbers, and hyphens.'
                )
            )

        return value
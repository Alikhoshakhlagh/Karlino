from rest_framework import serializers

from .models import Favorite
from drf_spectacular.utils import extend_schema_field


class FavoriteSerializer(serializers.ModelSerializer):
    project_title = serializers.CharField(source='project.title', read_only=True)
    project_owner_name = serializers.CharField(source='project.display_owner_name', read_only=True)
    project_company_name = serializers.SerializerMethodField()

    class Meta:
        model = Favorite
        fields = (
            'id',
            'project',
            'project_title',
            'project_owner_name',
            'project_company_name',
            'created_at',
        )
        read_only_fields = (
            'id',
            'project_title',
            'project_owner_name',
            'project_company_name',
            'created_at',
        )

    @extend_schema_field(serializers.CharField)
    def get_project_company_name(self, obj):
        return obj.project.company.name if obj.project.company else None
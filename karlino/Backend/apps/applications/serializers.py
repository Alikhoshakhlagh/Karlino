from rest_framework import serializers

from .models import Application
from ..core.messages import *

from drf_spectacular.utils import extend_schema_field


class ApplicationSerializer(serializers.ModelSerializer):
    applicant_name = serializers.CharField(source='applicant.full_name', read_only=True)
    project_title = serializers.CharField(source='project.title', read_only=True)
    project_owner_name = serializers.SerializerMethodField()
    project_company_name = serializers.SerializerMethodField()
    project = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Application
        fields = (
            'id',
            'applicant_name',
            'project_title',
            'project_owner_name',
            'project_company_name',
            'cover_letter',
            'proposed_price',
            'status',
            'created_at',
            'updated_at',
        )
        read_only_fields = (
            'id',
            'applicant_name',
            'project_title',
            'project_owner_name',
            'project_company_name',
            'status',
            'created_at',
            'updated_at',
        )

    @extend_schema_field(serializers.CharField)
    def get_project_owner_name(self, obj):
        return obj.project.display_owner_name

    @extend_schema_field(serializers.CharField)
    def get_project_company_name(self, obj):
        return obj.project.company.name if obj.project.company else None

    def validate(self, attrs):
        request = self.context['request']
        project = self.context.get('project')

        if project is None:
            raise serializers.ValidationError(PROJECT_REQUIRED)

        if project.creator_id == request.user.id:
            raise serializers.ValidationError(OWN_PROJECT_BID_REVIEWED)

        if project.company and project.company.owner_id == request.user.id:
            raise serializers.ValidationError(OWN_COMPANY_BID_REVIEWED)

        if Application.objects.filter(project=project, applicant=request.user).exists():
            raise serializers.ValidationError(ALREADY_APPLIED)

        proposed_price = attrs.get('proposed_price')

        if proposed_price is not None:

            if project.budget_min and proposed_price < project.budget_min:
                raise serializers.ValidationError({
                    'proposed_price': PRICE_BELOW_BUDGET
                })

            if project.budget_max and proposed_price > project.budget_max:
                raise serializers.ValidationError({
                    'proposed_price': PRICE_ABOVE_BUDGET
                })

        return attrs


    def create(self, validated_data):
        validated_data['applicant'] = self.context['request'].user
        validated_data['project'] = self.context['project']
        return super().create(validated_data)
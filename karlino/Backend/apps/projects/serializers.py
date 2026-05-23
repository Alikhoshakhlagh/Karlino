from datetime import date

from rest_framework import serializers

from drf_spectacular.utils import extend_schema_field

from apps.skills.models import Skill
from apps.categories.models import Category
from apps.categories.serializers import CategorySerializer

from .models import Project


class ProjectSerializer(serializers.ModelSerializer):

    creator_name = serializers.SerializerMethodField()

    creator_email = serializers.EmailField(
        source='creator.email',
        read_only=True,
    )

    company_name = serializers.CharField(
        source='company.name',
        read_only=True,
    )

    primary_category_name = serializers.CharField(
        source='primary_category.name',
        read_only=True,
    )

    primary_category_data = CategorySerializer(
        source='primary_category',
        read_only=True,
    )

    categories_data = CategorySerializer(
        source='categories',
        many=True,
        read_only=True,
    )

    skill_ids = serializers.PrimaryKeyRelatedField(
        source='skills',
        queryset=Skill.objects.all(),
        many=True,
        write_only=True,
        required=False,
    )

    category_ids = serializers.PrimaryKeyRelatedField(
        source='categories',
        queryset=Category.objects.all(),
        many=True,
        write_only=True,
        required=False,
    )

    primary_category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
    )

    skills = serializers.SerializerMethodField()

    display_owner_name = serializers.CharField(
        read_only=True,
    )

    is_company_project = serializers.BooleanField(
        read_only=True,
    )

    favorites_count = serializers.IntegerField(
        read_only=True,
        default=0,
    )

    applications_count = serializers.IntegerField(
        read_only=True,
        default=0,
    )

    class Meta:

        model = Project

        fields = (
            'id',

            'creator_name',
            'creator_email',

            'owner_type',

            'company',
            'company_name',

            'primary_category',
            'primary_category_name',
            'primary_category_data',

            'categories_data',
            'category_ids',

            'title',
            'description',

            'budget_min',
            'budget_max',

            'location',

            'deadline',

            'status',

            'skills',
            'skill_ids',

            'favorites_count',
            'applications_count',

            'display_owner_name',
            'is_company_project',

            'created_at',
            'updated_at',
        )

        read_only_fields = (
            'id',

            'creator_name',
            'creator_email',

            'company_name',

            'favorites_count',
            'applications_count',

            'display_owner_name',
            'is_company_project',

            'created_at',
            'updated_at',
        )

    @extend_schema_field(serializers.CharField)
    def get_creator_name(self, obj):

        return (
            f'{obj.creator.first_name} '
            f'{obj.creator.last_name}'
        ).strip()

    @extend_schema_field(
        {
            'type': 'array',
            'items': {
                'type': 'object',
                'properties': {
                    'id': {'type': 'integer'},
                    'name': {'type': 'string'},
                    'slug': {'type': 'string'},
                }
            }
        }
    )
    def get_skills(self, obj):

        return [
            {
                'id': skill.id,
                'name': skill.name,
                'slug': skill.slug,
            }
            for skill in obj.skills.all()
        ]

    def validate(self, attrs):

        request = self.context['request']

        user = request.user

        owner_type = attrs.get('owner_type') or (
            Project.OwnerType.COMPANY
            if hasattr(user, 'company')
            else Project.OwnerType.PERSONAL
        )

        company = attrs.get('company')

        user_company = getattr(
            user,
            'company',
            None,
        )

        if owner_type == Project.OwnerType.COMPANY:

            if not user_company and not company:

                raise serializers.ValidationError(
                    'You do not have a company profile yet.'
                )

            if company and company.owner_id != user.id:

                raise serializers.ValidationError(
                    'You can only post using your own company.'
                )

            attrs['company'] = company or user_company

        elif owner_type == Project.OwnerType.PERSONAL:

            if company is not None:

                raise serializers.ValidationError(
                    'Personal projects must not have a company.'
                )

            attrs['company'] = None

        budget_min = attrs.get('budget_min')

        budget_max = attrs.get('budget_max')

        if (
            budget_min is not None
            and budget_max is not None
            and budget_min > budget_max
        ):

            raise serializers.ValidationError(
                'budget_min cannot be greater than budget_max.'
            )

        deadline = attrs.get('deadline')

        if (
            deadline is not None
            and deadline < date.today()
        ):

            raise serializers.ValidationError(
                'deadline cannot be in the past.'
            )

        primary_category = attrs.get(
            'primary_category',
            getattr(self.instance, 'primary_category', None)
        )

        categories = attrs.get(
            'categories',
            list(
                self.instance.categories.all()
            ) if self.instance else []
        )

        if (
            primary_category
            and primary_category not in categories
        ):
            categories.append(primary_category)

        attrs['categories'] = categories

        attrs['owner_type'] = owner_type

        return attrs

    def create(self, validated_data):

        validated_data['creator'] = (
            self.context['request'].user
        )

        return super().create(validated_data)

    def update(self, instance, validated_data):

        validated_data.pop(
            'creator',
            None,
        )

        return super().update(
            instance,
            validated_data,
        )
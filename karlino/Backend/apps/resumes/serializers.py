from rest_framework import serializers

from ..skills.models import Skill
from ..core.messages import *

from .models import Resume, ResumeExperience


class ResumeExperienceSerializer(serializers.ModelSerializer):

    class Meta:

        model = ResumeExperience

        fields = (
            'id',
            'title',
            'company',
            'description',
            'start_date',
            'end_date',
            'created_at',
            'updated_at',
        )

        read_only_fields = (
            'id',
            'created_at',
            'updated_at',
        )


class SkillItemSerializer(serializers.ModelSerializer):

    class Meta:

        model = Skill

        fields = (
            'id',
            'name',
        )


class ResumeSerializer(serializers.ModelSerializer):

    skills = serializers.PrimaryKeyRelatedField(
        queryset=Skill.objects.all(),
        many=True,
        required=False,
        write_only=True,
    )

    skills_detail = SkillItemSerializer(
        source='skills',
        many=True,
        read_only=True,
    )

    experiences = ResumeExperienceSerializer(
        many=True,
        read_only=True,
    )

    full_name = serializers.CharField(
        source='user.full_name',
        read_only=True,
    )

    class Meta:

        model = Resume

        fields = (
            'id',
            'full_name',
            'headline',
            'about',
            'city',
            'website',
            'github',
            'is_public',
            'skills',
            'skills_detail',
            'experiences',
            'created_at',
            'updated_at',
        )

        read_only_fields = (
            'id',
            'full_name',
            'created_at',
            'updated_at',
        )

from django.db.models import Count, Q
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from drf_spectacular.utils import extend_schema_field

from ..accounts.models import User, UserSession
from ..applications.models import Application
from ..bids.models import Bid
from ..bids.serializers import WonBidSerializer
from ..core.messages import *
from ..favorites.models import Favorite
from ..projects.models import Project


class PersianTokenObtainPairSerializer(
    TokenObtainPairSerializer
):

    default_error_messages = {
        'no_active_account': INVALID_CREDENTIALS,
    }


class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True,
        min_length=8,
    )

    confirm_password = serializers.CharField(
        write_only=True,
        min_length=8,
    )

    class Meta:

        model = User

        fields = (
            'first_name',
            'last_name',
            'email',
            'password',
            'confirm_password',
            'gender',
            'date_of_birth',
        )

    def validate(self, attrs):

        if attrs['password'] != attrs['confirm_password']:

            raise serializers.ValidationError({
                'confirm_password': (
                    PASSWORD_NOT_MATCH
                )
            })

        return attrs

    def create(self, validated_data):

        validated_data.pop('confirm_password')

        password = validated_data.pop('password')

        return User.objects.create_user(
            password=password,
            **validated_data,
        )


class ProfileSerializer(serializers.ModelSerializer):

    full_name = serializers.SerializerMethodField()

    class Meta:

        model = User

        fields = (
            'id',
            'email',
            'full_name',
            'phone',
            'avatar',
            'first_name',
            'last_name',
            'gender',
            'date_of_birth',
        )

        read_only_fields = (
            'id',
            'email',
        )

    @extend_schema_field(serializers.CharField)
    def get_full_name(self, obj):

        return (
            f'{obj.first_name} '
            f'{obj.last_name}'
        ).strip()


class ProfileDashboardSerializer(
    ProfileSerializer
):

    dashboard = serializers.SerializerMethodField()

    class Meta(ProfileSerializer.Meta):

        fields = (
            *ProfileSerializer.Meta.fields,
            'is_expert',
            'dashboard',
        )

    def get_dashboard(self, obj):
        project_stats = Project.objects.filter(
            creator=obj,
        ).aggregate(

            my_projects_count=Count('id'),

            active_projects_count=Count(
                'id',
                filter=Q(
                    status=Project.Status.ACTIVE,
                ),
            ),

            approved_projects_count=Count(
                'id',
                filter=Q(
                    review_status=Project.ReviewStatus.APPROVED,
                ),
            ),

            pending_projects_count=Count(
                'id',
                filter=Q(
                    review_status=Project.ReviewStatus.PENDING,
                ),
            ),

            needs_revision_projects_count=Count(
                'id',
                filter=Q(
                    review_status=Project.ReviewStatus.NEEDS_REVISION,
                ),
            ),
        )

        return {
            **project_stats,

            'favorites_count': Favorite.objects.filter(
                user=obj,
            ).count(),

            'my_applications_count': Application.objects.filter(
                applicant=obj,
            ).count(),

            'my_bids_count': Bid.objects.filter(
                freelancer=obj,
            ).count(),
        }


class DashboardSerializer(
    serializers.Serializer
):

    my_projects_count = serializers.IntegerField()

    active_projects_count = serializers.IntegerField()

    approved_projects_count = serializers.IntegerField()

    pending_projects_count = serializers.IntegerField()

    needs_revision_projects_count = serializers.IntegerField()

    favorites_count = serializers.IntegerField()

    my_applications_count = serializers.IntegerField()

    my_bids_count = serializers.IntegerField()

    pending_review_projects_count = serializers.IntegerField(
        required=False
    )

class ChangePasswordSerializer(
    serializers.Serializer
):

    old_password = serializers.CharField(
        write_only=True,
    )

    new_password = serializers.CharField(
        write_only=True,
        min_length=8,
        error_messages={
            'min_length': PASSWORD_TOO_SHORT,
        },
    )

    confirm_password = serializers.CharField(
        write_only=True,
        min_length=8,
        error_messages={
            'min_length': PASSWORD_TOO_SHORT,
        },
    )

    def validate_old_password(self, value):

        user = self.context['request'].user

        if not user.check_password(value):

            raise serializers.ValidationError(
                OLD_PASSWORD_INCORRECT
            )

        return value

    def validate_new_password(self, value):

        validate_password(value)

        return value

    def validate(self, attrs):

        if (
            attrs['new_password']
            != attrs['confirm_password']
        ):

            raise serializers.ValidationError({
                'confirm_password': (
                    PASSWORD_NOT_MATCH
                )
            })

        return attrs


class UserSessionSerializer(
    serializers.ModelSerializer
):

    class Meta:

        model = UserSession

        fields = (
            'id',
            'user_agent',
            'ip_address',
            'created_at',
            'updated_at',
            'expires_at',
        )

        read_only_fields = fields

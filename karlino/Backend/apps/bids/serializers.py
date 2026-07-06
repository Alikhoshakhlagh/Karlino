from rest_framework import serializers

from drf_spectacular.utils import extend_schema_field

from .models import Bid
from ..core.messages import *


class BidCreateSerializer(serializers.ModelSerializer):

    amount = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        min_value=1,
        error_messages={
            'required': BID_AMOUNT_INVALID,
            'invalid': BID_AMOUNT_INVALID,
            'min_value': BID_AMOUNT_INVALID,
        },
    )

    delivery_days = serializers.IntegerField(
        min_value=1,
        error_messages={
            'required': BID_DELIVERY_INVALID,
            'invalid': BID_DELIVERY_INVALID,
            'min_value': BID_DELIVERY_INVALID,
        },
    )

    cover_letter = serializers.CharField(
        error_messages={
            'required': COVER_LETTER_REQUIRED,
            'blank': COVER_LETTER_REQUIRED,
        },
    )

    class Meta:

        model = Bid

        fields = (
            'amount',
            'delivery_days',
            'cover_letter',
        )


class BidSerializer(serializers.ModelSerializer):

    freelancer_name = serializers.CharField(
        source='freelancer.full_name',
        read_only=True,
    )

    freelancer_id = serializers.UUIDField(
        source='freelancer.id',
        read_only=True,
    )

    class Meta:

        model = Bid

        fields = (
            'id',
            'amount',
            'delivery_days',
            'cover_letter',
            'status',
            'price_score',
            'experience_score',
            'expert_score',
            'score_note',
            'employer_message',
            'employer_message_at',
            'freelancer_id',
            'freelancer_name',
            'created_at',
            'updated_at',
        )

        read_only_fields = fields


class PublicBidSerializer(serializers.ModelSerializer):

    freelancer_name = serializers.CharField(
        source='freelancer.full_name',
        read_only=True,
    )

    class Meta:

        model = Bid

        fields = (
            'id',
            'freelancer_name',
            'amount',
            'delivery_days',
            'status',
            'expert_score',
            'created_at',
        )

        read_only_fields = fields


class PublicWonBidSerializer(serializers.ModelSerializer):

    project_title = serializers.CharField(
        source='project.title',
        read_only=True,
    )

    class Meta:

        model = Bid

        fields = (
            'id',
            'project_title',
            'expert_score',
            'accepted_at',
        )

        read_only_fields = fields


class MyBidSerializer(serializers.ModelSerializer):


    project_title = serializers.CharField(
        source='project.title',
        read_only=True,
    )

    project_id = serializers.UUIDField(
        source='project.id',
        read_only=True,
    )

    class Meta:

        model = Bid

        fields = (
            'id',
            'project_id',
            'project_title',
            'amount',
            'delivery_days',
            'status',
            'price_score',
            'experience_score',
            'expert_score',
            'employer_message',
            'employer_message_at',
            'created_at',
            'updated_at',
        )

        read_only_fields = fields


class IncomingBidSerializer(serializers.ModelSerializer):

    freelancer_id = serializers.UUIDField(
        source='freelancer.id',
        read_only=True,
    )

    freelancer_name = serializers.CharField(
        source='freelancer.full_name',
        read_only=True,
    )

    project_id = serializers.UUIDField(
        source='project.id',
        read_only=True,
    )

    project_title = serializers.CharField(
        source='project.title',
        read_only=True,
    )

    class Meta:

        model = Bid

        fields = (
            'id',
            'project_id',
            'project_title',
            'freelancer_id',
            'freelancer_name',
            'amount',
            'delivery_days',
            'cover_letter',
            'status',
            'price_score',
            'experience_score',
            'expert_score',
            'employer_message',
            'employer_message_at',
            'created_at',
            'updated_at',
        )

        read_only_fields = fields


class ExpertBidSerializer(serializers.ModelSerializer):


    freelancer_id = serializers.UUIDField(
        source='freelancer.id',
        read_only=True,
    )

    freelancer_name = serializers.CharField(
        source='freelancer.full_name',
        read_only=True,
    )

    project_id = serializers.UUIDField(
        source='project.id',
        read_only=True,
    )

    project_title = serializers.CharField(
        source='project.title',
        read_only=True,
    )

    project_category = serializers.CharField(
        source='project.primary_category.name',
        read_only=True,
    )

    budget_min = serializers.DecimalField(
        source='project.budget_min',
        max_digits=12,
        decimal_places=2,
        read_only=True,
    )

    budget_max = serializers.DecimalField(
        source='project.budget_max',
        max_digits=12,
        decimal_places=2,
        read_only=True,
    )

    freelancer_history = serializers.SerializerMethodField()

    class Meta:

        model = Bid

        fields = (
            'id',
            'project_id',
            'project_title',
            'project_category',
            'budget_min',
            'budget_max',
            'freelancer_id',
            'freelancer_name',
            'freelancer_history',
            'amount',
            'delivery_days',
            'cover_letter',
            'created_at',
        )

        read_only_fields = fields

    @extend_schema_field(
        {
            'type': 'object',
            'properties': {
                'total_bids': {'type': 'integer'},
                'won_bids': {'type': 'integer'},
                'average_score': {'type': 'number', 'nullable': True},
            },
        }
    )
    def get_freelancer_history(self, obj):

        stats = self.context.get('freelancer_stats', {})

        default = {
            'total_bids': 0,
            'won_bids': 0,
            'average_score': None,
        }

        return stats.get(obj.freelancer_id, default)


class BidScoreSerializer(serializers.Serializer):

    price_score = serializers.IntegerField(
        min_value=1,
        max_value=5,
        error_messages={
            'required': PRICE_SCORE_INVALID,
            'invalid': PRICE_SCORE_INVALID,
            'min_value': PRICE_SCORE_INVALID,
            'max_value': PRICE_SCORE_INVALID,
        },
    )

    experience_score = serializers.IntegerField(
        min_value=1,
        max_value=5,
        error_messages={
            'required': EXPERIENCE_SCORE_INVALID,
            'invalid': EXPERIENCE_SCORE_INVALID,
            'min_value': EXPERIENCE_SCORE_INVALID,
            'max_value': EXPERIENCE_SCORE_INVALID,
        },
    )

    note = serializers.CharField(
        required=False,
        allow_blank=True,
    )


class EmployerMessageSerializer(serializers.Serializer):

    message = serializers.CharField(
        error_messages={
            'required': EMPLOYER_MESSAGE_EMPTY,
            'blank': EMPLOYER_MESSAGE_EMPTY,
        },
    )


class WonBidSerializer(serializers.ModelSerializer):

    project_id = serializers.UUIDField(
        source='project.id',
        read_only=True,
    )

    project_title = serializers.CharField(
        source='project.title',
        read_only=True,
    )

    class Meta:

        model = Bid

        fields = (
            'id',
            'project_id',
            'project_title',
            'amount',
            'delivery_days',
            'price_score',
            'experience_score',
            'expert_score',
            'accepted_at',
        )

        read_only_fields = fields

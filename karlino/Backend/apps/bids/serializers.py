from rest_framework import serializers

from .models import Bid

class BidSerializer(serializers.ModelSerializer):
    freelancer_name = serializers.CharField(source='freelancer.full_name', read_only=True)
    freelancer_id = serializers.UUIDField(source='freelancer.id',read_only=True)


    class Meta:
        model = Bid

        fields = (
            'id',
            'amount',
            'delivery_days',
            'cover_letter',
            'status',
            'freelancer_id',
            'freelancer_name',
            'created_at',
            'updated_at',
        )
        read_only_field = (
            'id',
            'status',
            'freelancer_name',
            'created_at',
            'updated_at',
        )


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
            'created_at',
        )
from rest_framework import serializers

from .models import Bid

class BidSerializer(serializers.ModelSerializer):
    freelancer_name = serializers.CharField(source='freelancer.full_name', read_only=True)

    class Meta:
        model = Bid

        fields = (
            'id',
            'amount',
            'delivery_days',
            'cover_letter',
            'status',
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
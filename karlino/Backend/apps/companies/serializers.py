from rest_framework import serializers
from .models import Company


class CompanySerializer(serializers.ModelSerializer):
    owner_email = serializers.EmailField(source='owner.email', read_only=True)
    owner_name = serializers.CharField(source='owner.full_name', read_only=True)

    class Meta:
        model = Company
        fields = (
            'id',
            'owner_email',
            'owner_name',
            'name',
            'description',
            'website',
            'logo',
            'phone',
            'address',
            'is_verified',
            'created_at',
            'updated_at',
        )
        read_only_fields = (
            'id',
            'owner_email',
            'owner_name',
            'is_verified',
            'created_at',
            'updated_at',
        )
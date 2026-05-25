from rest_framework import serializers

from drf_spectacular.utils import extend_schema_field

from apps.accounts.models import User


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
                    'Passwords do not match.'
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
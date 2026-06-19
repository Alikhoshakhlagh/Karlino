from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from ..core.messages import *

class ResetPasswordSerializer(
    serializers.Serializer
):

    email = serializers.EmailField()

    new_password = serializers.CharField(
        write_only=True,
    )

    confirm_password = serializers.CharField(
        write_only=True,
    )

    def validate_new_password(
        self,
        value,
    ):

        validate_password(value)

        return value

    def validate(
        self,
        attrs,
    ):

        if (
            attrs['new_password']
            != attrs['confirm_password']
        ):

            raise serializers.ValidationError(
                {
                    'confirm_password': (
                        PASSWORD_NOT_MATCH
                    )
                }
            )

        return attrs
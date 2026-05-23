from rest_framework import serializers


class ResetPasswordSerializer(serializers.Serializer):

    email = serializers.EmailField()

    new_password = serializers.CharField(
        min_length=8,
    )

    confirm_password = serializers.CharField(
        min_length=8,
    )

    def validate(self, attrs):

        if (
            attrs['new_password']
            != attrs['confirm_password']
        ):

            raise serializers.ValidationError({
                'confirm_password': (
                    'Passwords do not match.'
                )
            })

        return attrs
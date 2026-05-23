from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import (
    ResetPasswordSerializer
)

class ResetPasswordView(APIView):

    permission_classes = []

    serializer_class = ResetPasswordSerializer

    def post(self, request):

        serializer = self.serializer_class(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        email = serializer.validated_data['email']

        new_password = serializer.validated_data[
            'new_password'
        ]

        try:

            user = User.objects.get(
                email=email
            )

        except User.DoesNotExist:

            return Response(
                {
                    'detail': (
                        'User with this email '
                        'does not exist.'
                    )
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        user.set_password(new_password)

        user.save()

        return Response({
            'detail': (
                'Password reset successfully.'
            )
        })
from django.db.models import Q

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Application
from .serializers import ApplicationSerializer


class MyApplicationsAPIView(APIView):

    permission_classes = [IsAuthenticated]

    serializer_class = ApplicationSerializer

    def get(self, request):

        qs = (
            Application.objects
            .select_related(
                'project',
                'project__company',
                'project__creator',
                'project__primary_category',
            )
            .prefetch_related(
                'project__skills',
                'project__categories',
            )
            .filter(
                applicant=request.user
            )
            .order_by('-created_at')
        )

        serializer = self.serializer_class(
            qs,
            many=True,
        )

        return Response(serializer.data)


class IncomingApplicationsAPIView(APIView):

    permission_classes = [IsAuthenticated]

    serializer_class = ApplicationSerializer

    def get(self, request):

        qs = (
            Application.objects
            .select_related(
                'project',
                'project__company',
                'project__creator',
                'project__primary_category',
                'applicant',
            )
            .prefetch_related(
                'project__skills',
                'project__categories',
            )
            .filter(
                Q(project__creator=request.user)
                | Q(project__company__owner=request.user)
            )
            .distinct()
            .order_by('-created_at')
        )

        serializer = self.serializer_class(
            qs,
            many=True,
        )

        return Response(serializer.data)
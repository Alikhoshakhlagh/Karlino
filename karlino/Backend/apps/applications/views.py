from django.db.models import Q
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Application
from .serializers import ApplicationSerializer
from ..core.messages import (
    PERMISSION_DENIED,
    APPLICATION_NOT_PENDING,
    APPLICATION_ACCEPTED,
    APPLICATION_REJECTED,
)


def is_application_project_owner(application, user):

    project = application.project

    if project.creator_id == user.id:
        return True

    if project.company and project.company.owner_id == user.id:
        return True

    return False


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


class ApplicationAcceptAPIView(APIView):
    """تأیید یک درخواست دریافتی توسط صاحب پروژه"""

    permission_classes = [IsAuthenticated]

    serializer_class = ApplicationSerializer

    def post(self, request, application_id):

        application = get_object_or_404(
            Application.objects.select_related(
                'project',
                'project__company',
            ),
            pk=application_id,
        )

        # فقط صاحب پروژه می‌تواند درخواست را تأیید کند
        if not is_application_project_owner(application, request.user):
            return Response(
                {'detail': PERMISSION_DENIED},
                status=status.HTTP_403_FORBIDDEN,
            )

        # فقط درخواست‌های «در انتظار» قابل تأیید هستند
        if application.status != Application.Status.PENDING:
            return Response(
                {'detail': APPLICATION_NOT_PENDING},
                status=status.HTTP_400_BAD_REQUEST,
            )

        application.status = Application.Status.ACCEPTED

        application.save(
            update_fields=[
                'status',
                'updated_at',
            ]
        )

        return Response(
            {'detail': APPLICATION_ACCEPTED},
        )


class ApplicationRejectAPIView(APIView):
    permission_classes = [IsAuthenticated]

    serializer_class = ApplicationSerializer

    def post(self, request, application_id):

        application = get_object_or_404(
            Application.objects.select_related(
                'project',
                'project__company',
            ),
            pk=application_id,
        )

        if not is_application_project_owner(application, request.user):
            return Response(
                {'detail': PERMISSION_DENIED},
                status=status.HTTP_403_FORBIDDEN,
            )

        if application.status != Application.Status.PENDING:
            return Response(
                {'detail': APPLICATION_NOT_PENDING},
                status=status.HTTP_400_BAD_REQUEST,
            )

        application.status = Application.Status.REJECTED

        application.save(
            update_fields=[
                'status',
                'updated_at',
            ]
        )

        return Response(
            {'detail': APPLICATION_REJECTED},
        )

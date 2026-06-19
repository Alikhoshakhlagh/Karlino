from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from ..projects.models import Project

from .models import Bid
from .serializers import BidSerializer, MyBidSerializer
from ..core.messages import *

from django.utils import timezone
from django.db import transaction


class CreateOrUpdateBidAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, project_id):

        project = Project.objects.get(
            pk=project_id
        )

        if (
                project.project_mode
                !=
                Project.ProjectMode.TENDER
        ):
            return Response(
                {
                    'detail':
                        PROJECT_NOT_TENDER
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        if (
                project.status
                !=
                Project.Status.ACTIVE
        ):
            return Response(
                {
                    'detail':
                        PROJECT_NOT_ACTIVE
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if (
            project.ReviewStatus
            !=
            Project.ReviewStatus.APPROVED
        ):
            return Response(
                {
                    'detail':
                        PROJECT_NOT_APPROVED
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        if (
                project.creator == request.user
        ):
            return Response(
                {
                    'detail':
                        OWN_PROJECT_BID_REVIEWED
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        bid, created = Bid.objects.update_or_create(
            project=project,
            freelancer=request.user,

            defaults={
                'amount': request.data.get('amount'),
                'delivery_days': request.data.get(
                    'delivery_days'
                ),
                'cover_letter': request.data.get(
                    'cover_letter'
                ),
            }
        )

        return Response(
            BidSerializer(bid).data,
            status=(
                status.HTTP_201_CREATED
                if created
                else status.HTTP_200_OK
            )
        )


class ProjectBidListAPIView(APIView):

    permission_classes = [
        IsAuthenticated,
    ]

    def get(self, request, project_id):

        project = get_object_or_404(
            Project,
            pk=project_id,
        )

        is_owner = (
            project.creator_id
            ==
            request.user.id
        )

        is_company_owner = (

            project.company

            and

            project.company.owner_id
            ==
            request.user.id
        )

        if not (

            is_owner

            or

            is_company_owner

            or

            request.user.is_superuser

        ):

            return Response(
                {
                    'detail':
                        PERMISSION_DENIED
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        bids = (

            Bid.objects

            .select_related(
                'freelancer',
            )

            .filter(
                project=project,
            )

            .order_by(
                'amount',
                'delivery_days',
            )
        )

        serializer = BidSerializer(
            bids,
            many=True,
        )

        return Response(
            serializer.data
        )


class AcceptBidAPIView(APIView):

    permission_classes = [
        IsAuthenticated,
    ]

    def post(
        self,
        request,
        project_id,
        bid_id,
    ):
        project = get_object_or_404(
            Project,
            pk=project_id,
        )
        bid = get_object_or_404(
            Bid,
            pk=bid_id,
            project=project,
        )
        is_owner = (
            project.creator_id
            ==
            request.user.id
        )

        is_company_owner = (

            project.company

            and

            project.company.owner_id
            ==
            request.user.id
        )

        if not (
            is_owner
            or
            is_company_owner
            or
            request.user.is_superuser
        ):
            return Response(
                {
                    'detail':
                        PERMISSION_DENIED
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        if (
            project.status
            ==
            Project.Status.CLOSED
        ):
            return Response(
                {
                    'detail':
                        PROJECT_NOT_ACTIVE
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        with transaction.atomic():
            bid.status = (
                Bid.Status.ACCEPTED
            )

            bid.accepted_at = (
                timezone.now()
            )

            bid.save()
        Bid.objects.filter(
            project=project,
        ).exclude(
            pk=bid.pk,
        ).update(
            status=Bid.Status.REJECTED,
        )
        project.status = (
            Project.Status.CLOSED
        )

        project.save(
            update_fields=[
                'status',
            ]
        )

        return Response(
            {
                'detail':
                    BID_ACCEPTED
            }
        )


class MyBidsAPIView(APIView):

    permission_classes = [
        IsAuthenticated,
    ]

    def get(self, request):

        bids = (
            Bid.objects
            .select_related('project')
            .filter(
                freelancer=request.user,
            )
            .order_by('-created_at')
        )

        serializer = MyBidSerializer(
            bids,
            many=True,
        )

        return Response(
            serializer.data
        )
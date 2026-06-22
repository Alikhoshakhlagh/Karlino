from django.db.models import Count, Q
from drf_spectacular.utils import extend_schema
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import (
    RegisterSerializer,
    ProfileSerializer, ProfileDashboardSerializer, DashboardSerializer,
)
from ..applications.models import Application
from ..bids.models import Bid
from ..favorites.models import Favorite
from ..projects.models import Project


class RegisterAPIView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

@extend_schema(
    responses=ProfileSerializer
)
class ProfileAPIView(APIView):

    serializer_class = ProfileSerializer

    permission_classes = [
        IsAuthenticated,
    ]

    def get(self, request):

        serializer = (
            ProfileDashboardSerializer(
                request.user
            )
        )

        return Response(
            serializer.data
        )


@extend_schema(
    responses=DashboardSerializer
)
class DashboardAPIView(APIView):

    serializer_class = DashboardSerializer

    permission_classes = [
        IsAuthenticated,
    ]

    def get(self, request):

        user = request.user

        project_stats = Project.objects.filter(
            creator=user,
        ).aggregate(

            my_projects_count=Count(
                'id',
            ),

            active_projects_count=Count(
                'id',
                filter=Q(
                    status=Project.Status.ACTIVE,
                ),
            ),

            approved_projects_count=Count(
                'id',
                filter=Q(
                    review_status=Project.ReviewStatus.APPROVED,
                ),
            ),

            pending_projects_count=Count(
                'id',
                filter=Q(
                    review_status=Project.ReviewStatus.PENDING,
                ),
            ),

            needs_revision_projects_count=Count(
                'id',
                filter=Q(
                    review_status=Project.ReviewStatus.NEEDS_REVISION,
                ),
            ),
        )

        data = {

            **project_stats,

            'favorites_count': Favorite.objects.filter(
                user=user,
            ).count(),

            'my_applications_count': Application.objects.filter(
                applicant=user,
            ).count(),

            'my_bids_count': Bid.objects.filter(
                freelancer=user,
            ).count(),
        }

        if user.is_expert:

            data[
                'pending_review_projects_count'
            ] = Project.objects.filter(
                review_status=Project.ReviewStatus.PENDING,
            ).count()

        return Response(
            data,
        )
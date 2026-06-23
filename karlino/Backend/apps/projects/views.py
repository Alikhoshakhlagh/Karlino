from datetime import datetime

from django.db.models import Q, Count
from django.utils import timezone

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from ..applications.serializers import ApplicationSerializer
from .models import Project, ProjectReview
from .permissions import IsProjectOwnerOrCompanyOwner
from .serializers import ProjectSerializer, ExpertProjectSerializer, ProjectReviewSerializer
from ..core.messages import *

from drf_spectacular.utils import (
    extend_schema,
    OpenApiParameter,
)

from ..core.permissions import IsExpert


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsProjectOwnerOrCompanyOwner]

    def get_queryset(self):
        qs = (
            Project.objects
            .select_related('creator', 'company', 'primary_category')
            .prefetch_related('skills','categories',)
            .all()
        )

        user = self.request.user
        action = getattr(self, 'action', None)

        if action == 'list':
            qs = qs.filter(
                status=Project.Status.ACTIVE,
                review_status=Project.ReviewStatus.APPROVED,
            )

        elif action == 'retrieve':
            if user.is_authenticated:
                qs = qs.filter(
                    Q(status=Project.Status.ACTIVE,review_status=Project.ReviewStatus.APPROVED,)
                    | Q(creator=user)
                    | Q(company__owner=user)
                ).distinct()
            else:
                qs = qs.filter(
                    status=Project.Status.ACTIVE,
                    review_status=Project.ReviewStatus.APPROVED,
                )

        elif action in ('update', 'partial_update', 'destroy'):
            if user.is_authenticated:
                qs = qs.filter(
                    Q(creator=user) | Q(company__owner=user)
                ).distinct()
            else:
                qs = qs.none()

        elif action == 'my_posted':
            if user.is_authenticated:
                qs = qs.filter(
                    Q(creator=user) | Q(company__owner=user)
                ).distinct()
            else:
                qs = qs.none()

        search = self.request.query_params.get('search')
        if search:
            qs = qs.filter(
                Q(categories__name__icontains=search)
                | Q(primary_category__name__icontains=search)
                | Q(skills__name__icontains=search)
                | Q(company__name__icontains=search)
                | Q(title__icontains=search)
                | Q(description__icontains=search)
                | Q(location__icontains=search)
            ).distinct()

        category = self.request.query_params.get('category')
        if category:
            qs = qs.filter(categories__id=category)

        skill = self.request.query_params.get('skill')
        if skill:
            qs = qs.filter(skills__id=skill)

        owner_type = self.request.query_params.get('owner_type')
        if owner_type:
            qs = qs.filter(owner_type=owner_type)

        location = self.request.query_params.get('location')
        if location:
            qs = qs.filter(location__icontains=location)

        status_param = self.request.query_params.get('status')
        if action == 'my_posted' and status_param:
            qs = qs.filter(status=status_param)

        min_budget = self.request.query_params.get('min_budget')
        if min_budget:
            qs = qs.filter(budget_max__gte=min_budget)

        max_budget = self.request.query_params.get('max_budget')
        if max_budget:
            qs = qs.filter(budget_min__lte=max_budget)

        ordering = self.request.query_params.get(
            'ordering',
            'newest',
        )

        allowed_ordering = {

            # Date
            'newest': '-created_at',
            'oldest': 'created_at',

            # Budget
            'lowest_budget': 'budget_min',
            'highest_budget': '-budget_max',

            # Title
            'title': 'title',
            '-title': '-title',

            # Deadline
            'deadline': 'deadline',
            '-deadline': '-deadline',
        }

        if ordering == 'popular':

            qs = qs.annotate(

                favorites_count=Count(
                    'favorites',
                    distinct=True,
                ),

                applications_count=Count(
                    'applications',
                    distinct=True,
                ),
            ).order_by(
                '-favorites_count',
                '-applications_count',
                '-created_at',
            )

        else:

            qs = qs.order_by(
                allowed_ordering.get(
                    ordering,
                    '-created_at',
                )
            )

        return qs

    def perform_create(self, serializer):

        serializer.save(
            status=Project.Status.DRAFT,
            review_status=Project.ReviewStatus.PENDING,
        )

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_posted(self, request):

        qs = (
            Project.objects
            .select_related('creator', 'company', 'primary_category')
            .prefetch_related('skills','categories')
            .filter(
                Q(creator=request.user)
                | Q(company__owner=request.user)
            )
            .distinct()
            .order_by('-created_at')
        )

        status_param = request.query_params.get('status')

        if status_param:
            qs = qs.filter(status=status_param)

        serializer = self.get_serializer(qs, many=True)

        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def apply(self, request, pk=None):
        project = self.get_object()

        if project.status != Project.Status.ACTIVE:
            return Response(
                {'detail': PROJECT_NOT_ACTIVE},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if project.review_status != Project.ReviewStatus.APPROVED:
            return Response(
                {'detail': PROJECT_NOT_APPROVED},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = ApplicationSerializer(
            data=request.data,
            context={'request': request, 'project': project},
        )
        serializer.is_valid(raise_exception=True)
        application = serializer.save()

        return Response(
            ApplicationSerializer(application).data,
            status=status.HTTP_201_CREATED,
        )

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='limit',
                type=int,
                location=OpenApiParameter.QUERY,
                description='Number of popular projects',
                default=10,
            ),
        ],

        responses=ProjectSerializer(many=True),

        description='Get most popular projects.',
    )
    @action(detail=False,methods=['get'],url_path='popular',)
    def popular(self, request):

        limit = request.query_params.get(
            'limit',
            10,
        )

        try:
            limit = int(limit)
        except ValueError:
            limit = 10

        qs = (
            Project.objects
            .select_related(
                'creator',
                'company',
                'primary_category',
            )
            .prefetch_related(
                'skills',
                'categories',
            )
            .filter(
                status=Project.Status.ACTIVE,
                review_status=Project.ReviewStatus.APPROVED,
            )
            .annotate(
                favorites_count=Count(
                    'favorites',
                    distinct=True,
                ),

                applications_count=Count(
                    'applications',
                    distinct=True,
                ),
            )
            .order_by(
                '-favorites_count',
                '-applications_count',
                '-created_at',
            )[:limit]
        )

        serializer = self.get_serializer(
            qs,
            many=True,
        )

        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])

    def resubmit(self, request, pk=None):

        project = self.get_object()

        if (
                project.creator != request.user
                and
                (
                        not project.company
                        or
                        project.company.owner != request.user
                )
        ):
            return Response(
                {
                    'detail': PERMISSION_DENIED
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        if project.review_status != Project.ReviewStatus.NEEDS_REVISION:
            return Response(
                {
                    'detail': (
                        PROJECT_NOT_NEEDS_REVISION
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        project.review_status = (
            Project.ReviewStatus.PENDING
        )

        project.reviewed_by = None
        project.reviewed_at = None

        project.save(
            update_fields=[
                'review_status',
                'reviewed_by',
                'reviewed_at',
            ]
        )

        return Response(
            {
                'detail': (
                    PROJECT_SUBMITTED_FOR_REVIEW
                )
            }
        )

    @action(
        detail=True,
        methods=['post'],
        url_path='expert/review',
        permission_classes=[
            IsAuthenticated,
            IsExpert,
        ],
    )
    def review(self, request, pk=None):
        project = self.get_object()

        serializer = ProjectReviewSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        review_status = serializer.validated_data[
            'status'
        ]

        comment = serializer.validated_data.get(
            'comment',
            ''
        )

        if (
                project.review_status
                !=
                Project.ReviewStatus.PENDING
        ):
            return Response(
                {
                    'detail':
                        PROJECT_ALREADY_REVIEWED
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if (
                project.creator
                ==
                request.user
        ):
            return Response(
                {
                    'detail':
                        OWN_PROJECT_BID_REVIEWED
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if(
                project.primary_category
                not in
                request.user.expert_categories.all()
        ):
            return Response(
                {
                    'detail':
                        EXPERT_CATEGORY_DENIED
                },
                status=status.HTTP_403_FORBIDDEN,
            )
        ProjectReview.objects.create(
            project=project,
            expert=request.user,
            status=review_status,
            comment=comment,
        )

        project.review_status = review_status
        project.reviewed_by = request.user
        project.reviewed_at = timezone.now()

        if (
                review_status
                ==
                ProjectReview.Status.APPROVED
        ):

            project.status = (
                Project.Status.ACTIVE
            )

        elif (
                review_status
                ==
                ProjectReview.Status.REJECTED
        ):

            project.status = (
                Project.Status.ARCHIVED
            )

        elif (
                review_status
                ==
                ProjectReview.Status.NEEDS_REVISION
        ):

            project.status = (
                Project.Status.DRAFT
            )

        project.save()

        return Response(
            {
                'detail':
                    REVIEW_SUBMITTED
            }
        )


#REVIEW
class PendingProjectsAPIView(APIView):

    serializer_class = ExpertProjectSerializer

    permission_classes = [
        IsAuthenticated,
        IsExpert,
    ]
    def get(self, request):
        expert_categories = (
            request.user.expert_categories.all()
        )

        qs = (
            Project.objects.select_related(
                'creator',
                'company',
                'primary_category',
            )
            .prefetch_related(
                'skills',
                'categories',
            )
            .filter(
                review_status=Project.ReviewStatus.PENDING,
                primary_category__in=expert_categories,
            )
        )

        serializer = ExpertProjectSerializer(
            qs,
            many=True,
        )

        return Response(serializer.data)


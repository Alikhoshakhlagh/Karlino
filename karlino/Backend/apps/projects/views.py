from django.db.models import Q, Count

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from apps.applications.serializers import ApplicationSerializer
from .models import Project
from .permissions import IsProjectOwnerOrCompanyOwner
from .serializers import ProjectSerializer

from drf_spectacular.utils import (
    extend_schema,
    OpenApiParameter,
)

class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsProjectOwnerOrCompanyOwner]

    def get_queryset(self):
        qs = (
            Project.objects
            .select_related('creator', 'company', 'primary_category')
            .prefetch_related('skills')
            .all()
        )

        user = self.request.user
        action = getattr(self, 'action', None)

        if action == 'list':
            qs = qs.filter(status=Project.Status.ACTIVE)

        elif action == 'retrieve':
            if user.is_authenticated:
                qs = qs.filter(
                    Q(status=Project.Status.ACTIVE)
                    | Q(creator=user)
                    | Q(company__owner=user)
                ).distinct()
            else:
                qs = qs.filter(status=Project.Status.ACTIVE)

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
                Q(category__name__icontains=search)
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
        if status_param:
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
        # qs = qs.order_by(allowed_ordering.get(ordering, '-created_at'))

        return qs

    def perform_create(self, serializer):
        serializer.save()

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_posted(self, request):

        qs = (
            Project.objects
            .select_related('creator', 'company', 'primary_category')
            .prefetch_related('skills')
            .filter(
                Q(creator=request.user)
                | Q(company__owner=request.user)
            )
            .distinct()
            .order_by('-created_at')
        )

        serializer = self.get_serializer(qs, many=True)

        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def apply(self, request, pk=None):
        project = self.get_object()

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
    @action(
        detail=False,
        methods=['get'],
        url_path='popular',
    )
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
                status=Project.Status.ACTIVE
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
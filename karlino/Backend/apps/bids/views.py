from decimal import Decimal

from django.db import transaction
from django.db.models import Avg, Case, Count, IntegerField, Q, Value, When
from django.shortcuts import get_object_or_404
from django.utils import timezone

from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..core.messages import *
from ..core.permissions import IsExpert
from ..projects.models import Project

from .models import Bid
from .serializers import (
    BidCreateSerializer,
    BidSerializer,
    PublicBidSerializer,
    MyBidSerializer,
    IncomingBidSerializer,
    ExpertBidSerializer,
    BidScoreSerializer,
    EmployerMessageSerializer,
)


def is_project_owner(project, user):

    if project.creator_id == user.id:
        return True

    if (
        project.company
        and project.company.owner_id == user.id
    ):
        return True

    return False


def build_freelancer_stats(freelancer_ids):

    stats = {}

    rows = (
        Bid.objects
        .filter(
            freelancer_id__in=freelancer_ids,
        )
        .values(
            'freelancer_id',
        )
        .annotate(
            total_bids=Count('id'),
            won_bids=Count(
                'id',
                filter=Q(status=Bid.Status.ACCEPTED),
            ),
            average_score=Avg('expert_score'),
        )
    )

    for row in rows:

        average_score = row['average_score']

        if average_score is not None:
            average_score = round(average_score, 1)

        stats[row['freelancer_id']] = {
            'total_bids': row['total_bids'],
            'won_bids': row['won_bids'],
            'average_score': average_score,
        }

    return stats


class CreateOrUpdateBidAPIView(APIView):

    serializer_class = BidCreateSerializer

    permission_classes = [
        IsAuthenticated,
    ]

    def post(self, request, project_id):

        project = get_object_or_404(
            Project,
            pk=project_id,
        )

        if project.project_mode != Project.ProjectMode.TENDER:
            return Response(
                {'detail': PROJECT_NOT_TENDER},
                status=status.HTTP_400_BAD_REQUEST,
            )

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

        if is_project_owner(project, request.user):
            return Response(
                {'detail': OWN_PROJECT_BID_REVIEWED},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.serializer_class(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        existing_bid = Bid.objects.filter(
            project=project,
            freelancer=request.user,
        ).first()

        if (
            existing_bid is not None
            and existing_bid.status in (
                Bid.Status.ACCEPTED,
                Bid.Status.REJECTED,
            )
        ):
            return Response(
                {'detail': BID_LOCKED},
                status=status.HTTP_400_BAD_REQUEST,
            )

        bid, created = Bid.objects.update_or_create(
            project=project,
            freelancer=request.user,
            defaults={
                'amount': serializer.validated_data['amount'],
                'delivery_days': serializer.validated_data['delivery_days'],
                'cover_letter': serializer.validated_data['cover_letter'],
            },
        )

        return Response(
            BidSerializer(bid).data,
            status=(
                status.HTTP_201_CREATED
                if created
                else status.HTTP_200_OK
            ),
        )


class ProjectBidListAPIView(APIView):

    serializer_class = BidSerializer

    permission_classes = [
        IsAuthenticated,
    ]

    def get(self, request, project_id):

        project = get_object_or_404(
            Project,
            pk=project_id,
        )

        if project.project_mode != Project.ProjectMode.TENDER:
            return Response(
                {'detail': PROJECT_NOT_TENDER},
                status=status.HTTP_400_BAD_REQUEST,
            )

        bids = (
            Bid.objects
            .select_related('freelancer')
            .filter(project=project)
            .annotate(
                score_missing=Case(
                    When(
                        expert_score__isnull=True,
                        then=Value(1),
                    ),
                    default=Value(0),
                    output_field=IntegerField(),
                ),
            )
            .order_by(
                'score_missing',
                '-expert_score',
                'amount',
                'delivery_days',
            )
        )

        owner = (
            is_project_owner(project, request.user)
            or request.user.is_superuser
        )

        if owner:
            serializer_class = BidSerializer
        else:
            serializer_class = PublicBidSerializer

        winner = None

        for bid in bids:

            if bid.status == Bid.Status.ACCEPTED:
                winner = bid
                break

        winner_data = None

        if winner is not None:
            winner_data = serializer_class(winner).data

        serializer = serializer_class(
            bids,
            many=True,
        )

        return Response({
            'winner': winner_data,
            'bids': serializer.data,
        })


class AcceptBidAPIView(APIView):

    serializer_class = MyBidSerializer

    permission_classes = [
        IsAuthenticated,
    ]

    def post(self, request, project_id, bid_id):

        project = get_object_or_404(
            Project,
            pk=project_id,
        )

        bid = get_object_or_404(
            Bid,
            pk=bid_id,
            project=project,
        )

        if not (
            is_project_owner(project, request.user)
            or request.user.is_superuser
        ):
            return Response(
                {'detail': PERMISSION_DENIED},
                status=status.HTTP_403_FORBIDDEN,
            )

        if project.status == Project.Status.CLOSED:
            return Response(
                {'detail': PROJECT_NOT_ACTIVE},
                status=status.HTTP_400_BAD_REQUEST,
            )

        with transaction.atomic():

            bid.status = Bid.Status.ACCEPTED
            bid.accepted_at = timezone.now()
            bid.save()

            Bid.objects.filter(
                project=project,
            ).exclude(
                pk=bid.pk,
            ).update(
                status=Bid.Status.REJECTED,
            )

            project.status = Project.Status.CLOSED
            project.save(
                update_fields=['status'],
            )

        return Response(
            {'detail': BID_ACCEPTED},
        )


class BidMessageAPIView(APIView):

    serializer_class = EmployerMessageSerializer

    permission_classes = [
        IsAuthenticated,
    ]

    def post(self, request, project_id, bid_id):

        project = get_object_or_404(
            Project,
            pk=project_id,
        )

        bid = get_object_or_404(
            Bid,
            pk=bid_id,
            project=project,
        )

        if not is_project_owner(project, request.user):
            return Response(
                {'detail': PERMISSION_DENIED},
                status=status.HTTP_403_FORBIDDEN,
            )

        if bid.employer_message:
            return Response(
                {'detail': EMPLOYER_MESSAGE_ALREADY_SENT},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if bid.status not in (
            Bid.Status.PENDING,
            Bid.Status.SHORTLISTED,
        ):
            return Response(
                {'detail': BID_NOT_OPEN},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.serializer_class(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        bid.employer_message = serializer.validated_data['message']
        bid.employer_message_at = timezone.now()

        bid.save(
            update_fields=[
                'employer_message',
                'employer_message_at',
                'updated_at',
            ]
        )

        return Response(
            {'detail': EMPLOYER_MESSAGE_SENT},
        )


@extend_schema(
    responses=MyBidSerializer(many=True)
)
class MyBidsAPIView(APIView):

    serializer_class = MyBidSerializer

    permission_classes = [
        IsAuthenticated,
    ]

    def get(self, request):

        bids = (
            Bid.objects
            .select_related('project')
            .filter(freelancer=request.user)
            .order_by('-created_at')
        )

        serializer = self.serializer_class(
            bids,
            many=True,
        )

        return Response(serializer.data)


@extend_schema(
    responses=IncomingBidSerializer(many=True)
)
class IncomingBidsAPIView(APIView):

    serializer_class = IncomingBidSerializer

    permission_classes = [
        IsAuthenticated,
    ]

    def get(self, request):

        bids = (
            Bid.objects
            .select_related(
                'freelancer',
                'project',
                'project__company',
                'project__creator',
            )
            .filter(
                Q(project__creator=request.user)
                | Q(project__company__owner=request.user),
                project__project_mode=Project.ProjectMode.TENDER,
            )
            .distinct()
            .order_by('-created_at')
        )

        serializer = self.serializer_class(
            bids,
            many=True,
        )

        return Response(serializer.data)


@extend_schema(
    responses=ExpertBidSerializer(many=True)
)
class ExpertPendingBidsAPIView(APIView):

    serializer_class = ExpertBidSerializer

    permission_classes = [
        IsAuthenticated,
        IsExpert,
    ]

    def get(self, request):

        expert_categories = (
            request.user.expert_categories.all()
        )

        bids = (
            Bid.objects
            .select_related(
                'freelancer',
                'project',
                'project__primary_category',
            )
            .filter(
                expert_score__isnull=True,
                project__project_mode=Project.ProjectMode.TENDER,
                project__primary_category__in=expert_categories,
            )
            .exclude(
                project__creator=request.user,
            )
            .exclude(
                freelancer=request.user,
            )
            .order_by('-created_at')
        )

        freelancer_ids = []

        for bid in bids:

            if bid.freelancer_id not in freelancer_ids:
                freelancer_ids.append(bid.freelancer_id)

        stats = build_freelancer_stats(freelancer_ids)

        serializer = self.serializer_class(
            bids,
            many=True,
            context={'freelancer_stats': stats},
        )

        return Response(serializer.data)


class ScoreBidAPIView(APIView):

    serializer_class = BidScoreSerializer

    permission_classes = [
        IsAuthenticated,
        IsExpert,
    ]

    def post(self, request, project_id, bid_id):

        project = get_object_or_404(
            Project,
            pk=project_id,
        )

        bid = get_object_or_404(
            Bid,
            pk=bid_id,
            project=project,
        )

        if project.project_mode != Project.ProjectMode.TENDER:
            return Response(
                {'detail': PROJECT_NOT_TENDER},
                status=status.HTTP_400_BAD_REQUEST,
            )

        expert_categories = (
            request.user.expert_categories.all()
        )

        if project.primary_category not in expert_categories:
            return Response(
                {'detail': EXPERT_CATEGORY_DENIED},
                status=status.HTTP_403_FORBIDDEN,
            )

        if (
            is_project_owner(project, request.user)
            or bid.freelancer_id == request.user.id
        ):
            return Response(
                {'detail': SELF_SCORE_FORBIDDEN},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if bid.expert_score is not None:
            return Response(
                {'detail': BID_ALREADY_SCORED},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.serializer_class(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        price_score = serializer.validated_data['price_score']

        experience_score = serializer.validated_data['experience_score']

        average = (
            Decimal(price_score + experience_score)
            / Decimal(2)
        )

        bid.price_score = price_score
        bid.experience_score = experience_score
        bid.expert_score = average
        bid.score_note = serializer.validated_data.get('note', '')
        bid.scored_by = request.user
        bid.scored_at = timezone.now()

        bid.save(
            update_fields=[
                'price_score',
                'experience_score',
                'expert_score',
                'score_note',
                'scored_by',
                'scored_at',
                'updated_at',
            ]
        )

        return Response({
            'detail': BID_SCORE_SUBMITTED,
            'price_score': price_score,
            'experience_score': experience_score,
            'expert_score': str(average),
        })

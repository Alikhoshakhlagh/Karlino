from django.db.models import Avg, Count, Q
from django.shortcuts import get_object_or_404

from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..accounts.models import User
from ..applications.models import Application
from ..bids.models import Bid
from ..bids.serializers import WonBidSerializer, PublicWonBidSerializer
from ..core.messages import *

from .models import Resume, ResumeExperience
from .serializers import ResumeSerializer, ResumeExperienceSerializer


def build_site_history(user, public):
    """
    The trusted part of the resume, computed live from real
    site activity so the user cannot edit it.
    On public resumes only the average score is exposed.
    """

    bid_stats = Bid.objects.filter(
        freelancer=user,
    ).aggregate(
        total_bids=Count('id'),
        won_bids=Count(
            'id',
            filter=Q(status=Bid.Status.ACCEPTED),
        ),
        average_score=Avg('expert_score'),
    )

    average_score = bid_stats['average_score']

    if average_score is not None:
        average_score = round(average_score, 1)

    completed_projects = Application.objects.filter(
        applicant=user,
        status=Application.Status.ACCEPTED,
    ).count()

    won_bids = (
        Bid.objects
        .select_related('project')
        .filter(
            freelancer=user,
            status=Bid.Status.ACCEPTED,
        )
        .order_by('-accepted_at')
    )

    if public:
        won_serializer = PublicWonBidSerializer(
            won_bids,
            many=True,
        )
    else:
        won_serializer = WonBidSerializer(
            won_bids,
            many=True,
        )

    return {
        'member_since': user.created_at.date(),
        'total_bids': bid_stats['total_bids'],
        'won_bids_count': bid_stats['won_bids'],
        'average_score': average_score,
        'completed_simple_projects': completed_projects,
        'won_bids': won_serializer.data,
    }


class MyResumeAPIView(APIView):
    """
    The user's own resume: view, create, edit.
    """

    serializer_class = ResumeSerializer

    permission_classes = [
        IsAuthenticated,
    ]

    def get(self, request):

        resume = Resume.objects.filter(
            user=request.user,
        ).prefetch_related(
            'skills',
            'experiences',
        ).first()

        if resume is None:
            return Response({
                'resume': None,
                'site_history': build_site_history(
                    request.user,
                    public=False,
                ),
            })

        serializer = self.serializer_class(resume)

        return Response({
            'resume': serializer.data,
            'site_history': build_site_history(
                request.user,
                public=False,
            ),
        })

    def post(self, request):

        exists = Resume.objects.filter(
            user=request.user,
        ).exists()

        if exists:
            return Response(
                {'detail': RESUME_EXISTS},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.serializer_class(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        serializer.save(
            user=request.user,
        )

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )

    def patch(self, request):

        resume = Resume.objects.filter(
            user=request.user,
        ).first()

        if resume is None:
            return Response(
                {'detail': RESUME_NOT_FOUND},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = self.serializer_class(
            resume,
            data=request.data,
            partial=True,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        serializer.save()

        return Response(serializer.data)


class ResumeExperienceCreateAPIView(APIView):

    serializer_class = ResumeExperienceSerializer

    permission_classes = [
        IsAuthenticated,
    ]

    def post(self, request):

        resume = Resume.objects.filter(
            user=request.user,
        ).first()

        if resume is None:
            return Response(
                {'detail': RESUME_NOT_FOUND},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = self.serializer_class(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        serializer.save(
            resume=resume,
        )

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )


class ResumeExperienceDetailAPIView(APIView):

    serializer_class = ResumeExperienceSerializer

    permission_classes = [
        IsAuthenticated,
    ]

    def get_experience(self, request, experience_id):

        return get_object_or_404(
            ResumeExperience,
            pk=experience_id,
            resume__user=request.user,
        )

    def patch(self, request, experience_id):

        experience = self.get_experience(
            request,
            experience_id,
        )

        serializer = self.serializer_class(
            experience,
            data=request.data,
            partial=True,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        serializer.save()

        return Response(serializer.data)

    def delete(self, request, experience_id):

        experience = self.get_experience(
            request,
            experience_id,
        )

        experience.delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT,
        )


@extend_schema(
    responses={200: dict},
)
class PublicResumeAPIView(APIView):
    """
    Another user's resume, e.g. opened by an employer
    before accepting a bid. Only the average score is shown.
    """

    permission_classes = [
        IsAuthenticated,
    ]

    def get(self, request, user_id):

        user = get_object_or_404(
            User,
            pk=user_id,
        )

        resume = Resume.objects.filter(
            user=user,
        ).prefetch_related(
            'skills',
            'experiences',
        ).first()

        if resume is None:
            return Response(
                {'detail': RESUME_NOT_FOUND},
                status=status.HTTP_404_NOT_FOUND,
            )

        if (
            not resume.is_public
            and user.id != request.user.id
        ):
            return Response(
                {'detail': RESUME_PRIVATE},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = ResumeSerializer(resume)

        return Response({
            'resume': serializer.data,
            'site_history': build_site_history(
                user,
                public=True,
            ),
        })

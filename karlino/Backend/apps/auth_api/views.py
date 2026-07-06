from datetime import datetime, timezone as dt_timezone

from django.db.models import Count, Q
from django.utils import timezone
from drf_spectacular.utils import extend_schema
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.token_blacklist.models import (
    BlacklistedToken,
    OutstandingToken,
)

from .serializers import (
    RegisterSerializer,
    ProfileSerializer, ProfileDashboardSerializer, DashboardSerializer,
    ChangePasswordSerializer, UserSessionSerializer,
    PersianTokenObtainPairSerializer,
)
from ..accounts.models import UserSession
from ..applications.models import Application
from ..bids.models import Bid
from ..favorites.models import Favorite
from ..projects.models import Project
from ..core.messages import *


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

    def patch(self, request):

        serializer = ProfileSerializer(
            request.user,
            data=request.data,
            partial=True,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        serializer.save()

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

def get_client_ip(request):

    forwarded = request.META.get('HTTP_X_FORWARDED_FOR')

    if forwarded:
        return forwarded.split(',')[0].strip()

    return request.META.get('REMOTE_ADDR')


def get_user_agent(request):

    return request.META.get('HTTP_USER_AGENT', '')


def record_session(request, token):

    user_id = token.payload.get('user_id')
    jti = token.payload.get('jti')
    exp = token.payload.get('exp')

    if not user_id or not jti or not exp:
        return

    expires_at = datetime.fromtimestamp(
        exp,
        tz=dt_timezone.utc,
    )

    UserSession.objects.create(
        user_id=user_id,
        jti=jti,
        user_agent=get_user_agent(request),
        ip_address=get_client_ip(request),
        expires_at=expires_at,
    )


def blacklist_jti(jti):

    try:
        outstanding = OutstandingToken.objects.get(
            jti=jti,
        )

    except OutstandingToken.DoesNotExist:
        return

    BlacklistedToken.objects.get_or_create(
        token=outstanding,
    )


def revoke_all_sessions(user):

    sessions = UserSession.objects.filter(
        user=user,
        revoked=False,
    )

    for session in sessions:

        blacklist_jti(session.jti)

        session.revoked = True

        session.save(
            update_fields=[
                'revoked',
                'updated_at',
            ]
        )


class SessionTokenObtainPairView(TokenObtainPairView):

    serializer_class = PersianTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):

        response = super().post(
            request,
            *args,
            **kwargs,
        )

        if response.status_code != 200:
            return response

        refresh_str = response.data.get('refresh')

        if not refresh_str:
            return response

        try:
            token = RefreshToken(refresh_str)

        except TokenError:
            return response

        record_session(request, token)

        return response


class SessionTokenRefreshView(TokenRefreshView):

    def post(self, request, *args, **kwargs):

        old_refresh = request.data.get('refresh')

        old_jti = None

        if old_refresh:

            try:
                old_token = RefreshToken(old_refresh)
                old_jti = old_token.payload.get('jti')

            except TokenError:
                old_jti = None

        response = super().post(
            request,
            *args,
            **kwargs,
        )

        if response.status_code != 200:
            return response

        new_refresh = response.data.get('refresh')

        if not new_refresh:
            # rotation disabled, jti unchanged
            return response

        try:
            new_token = RefreshToken(new_refresh)

        except TokenError:
            return response

        new_jti = new_token.payload.get('jti')
        exp = new_token.payload.get('exp')

        if not new_jti or not exp:
            return response

        expires_at = datetime.fromtimestamp(
            exp,
            tz=dt_timezone.utc,
        )

        session = None

        if old_jti:
            session = UserSession.objects.filter(
                jti=old_jti,
                revoked=False,
            ).first()

        if session is not None:

            session.jti = new_jti
            session.expires_at = expires_at
            session.ip_address = get_client_ip(request)
            session.user_agent = get_user_agent(request)

            session.save(
                update_fields=[
                    'jti',
                    'expires_at',
                    'ip_address',
                    'user_agent',
                    'updated_at',
                ]
            )

        else:
            record_session(request, new_token)

        return response


class ChangePasswordAPIView(APIView):

    serializer_class = ChangePasswordSerializer

    permission_classes = [
        IsAuthenticated,
    ]

    def post(self, request):

        serializer = self.serializer_class(
            data=request.data,
            context={'request': request},
        )

        serializer.is_valid(
            raise_exception=True,
        )

        user = request.user

        user.set_password(
            serializer.validated_data['new_password']
        )

        user.save(
            update_fields=['password'],
        )

        # security: end every active session after a password change
        revoke_all_sessions(user)

        return Response({
            'detail': PASSWORD_CHANGED,
        })


@extend_schema(
    responses=UserSessionSerializer(many=True)
)
class SessionListAPIView(APIView):

    serializer_class = UserSessionSerializer

    permission_classes = [
        IsAuthenticated,
    ]

    def get(self, request):

        qs = UserSession.objects.filter(
            user=request.user,
            revoked=False,
            expires_at__gt=timezone.now(),
        ).order_by('-created_at')

        serializer = self.serializer_class(
            qs,
            many=True,
        )

        return Response(serializer.data)


@extend_schema(
    request=None,
    responses={200: dict},
)
class SessionRevokeAPIView(APIView):

    permission_classes = [
        IsAuthenticated,
    ]

    def post(self, request, session_id):

        session = UserSession.objects.filter(
            id=session_id,
            user=request.user,
            revoked=False,
        ).first()

        if session is None:
            return Response(
                {'detail': SESSION_NOT_FOUND},
                status=status.HTTP_404_NOT_FOUND,
            )

        blacklist_jti(session.jti)

        session.revoked = True

        session.save(
            update_fields=[
                'revoked',
                'updated_at',
            ]
        )

        return Response({
            'detail': SESSION_REVOKED,
        })


def month_key(value):

    return f'{value.year}-{value.month:02d}'


def last_months(count):

    now = timezone.now()

    months = []

    year = now.year
    month = now.month

    for i in range(count):

        months.append(f'{year}-{month:02d}')

        month = month - 1

        if month == 0:
            month = 12
            year = year - 1

    months.reverse()

    return months


def monthly_counts(queryset, months):

    counts = {}

    for month in months:
        counts[month] = 0

    for item in queryset:

        key = month_key(item.created_at)

        if key in counts:
            counts[key] = counts[key] + 1

    data = []

    for month in months:
        data.append(counts[month])

    return data


@extend_schema(
    responses={200: dict},
)
class ProfileChartsAPIView(APIView):

    permission_classes = [
        IsAuthenticated,
    ]

    def get(self, request):

        user = request.user

        project_status_labels = {
            Project.Status.DRAFT: 'پیش‌نویس',
            Project.Status.ACTIVE: 'فعال',
            Project.Status.CLOSED: 'بسته‌شده',
            Project.Status.COMPLETED: 'تکمیل‌شده',
            Project.Status.ARCHIVED: 'بایگانی',
        }

        my_projects = Project.objects.filter(
            Q(creator=user) | Q(company__owner=user)
        ).distinct()

        project_counts = {}

        for value in project_status_labels:
            project_counts[value] = 0

        for project in my_projects:

            if project.status in project_counts:
                project_counts[project.status] += 1

        projects_by_status = {
            'labels': [],
            'data': [],
        }

        for value in project_status_labels:
            projects_by_status['labels'].append(
                project_status_labels[value]
            )
            projects_by_status['data'].append(
                project_counts[value]
            )

        application_status_labels = {
            Application.Status.PENDING: 'در انتظار',
            Application.Status.ACCEPTED: 'پذیرفته‌شده',
            Application.Status.REJECTED: 'ردشده',
            Application.Status.WITHDRAWN: 'انصراف',
        }

        my_applications = Application.objects.filter(
            applicant=user,
        )

        application_counts = {}

        for value in application_status_labels:
            application_counts[value] = 0

        for application in my_applications:

            if application.status in application_counts:
                application_counts[application.status] += 1

        applications_by_status = {
            'labels': [],
            'data': [],
        }

        for value in application_status_labels:
            applications_by_status['labels'].append(
                application_status_labels[value]
            )
            applications_by_status['data'].append(
                application_counts[value]
            )

        bid_status_labels = {
            Bid.Status.PENDING: 'در انتظار',
            Bid.Status.SHORTLISTED: 'منتخب اولیه',
            Bid.Status.ACCEPTED: 'برنده',
            Bid.Status.REJECTED: 'ردشده',
            Bid.Status.WITHDRAWN: 'انصراف',
        }

        my_bids = Bid.objects.select_related(
            'project',
        ).filter(
            freelancer=user,
        )

        bid_counts = {}

        for value in bid_status_labels:
            bid_counts[value] = 0

        for bid in my_bids:

            if bid.status in bid_counts:
                bid_counts[bid.status] += 1

        bids_by_status = {
            'labels': [],
            'data': [],
        }

        for value in bid_status_labels:
            bids_by_status['labels'].append(
                bid_status_labels[value]
            )
            bids_by_status['data'].append(
                bid_counts[value]
            )

        won_bids_scores = {
            'labels': [],
            'data': [],
        }

        for bid in my_bids:

            if bid.status != Bid.Status.ACCEPTED:
                continue

            if bid.expert_score is None:
                continue

            won_bids_scores['labels'].append(
                bid.project.title
            )

            won_bids_scores['data'].append(
                bid.expert_score
            )

        months = last_months(6)

        monthly_activity = {
            'labels': months,
            'datasets': [
                {
                    'label': 'پروژه‌ها',
                    'data': monthly_counts(my_projects, months),
                },
                {
                    'label': 'درخواست‌ها',
                    'data': monthly_counts(my_applications, months),
                },
                {
                    'label': 'پیشنهادها',
                    'data': monthly_counts(my_bids, months),
                },
            ],
        }

        return Response({
            'projects_by_status': projects_by_status,
            'applications_by_status': applications_by_status,
            'bids_by_status': bids_by_status,
            'won_bids_scores': won_bids_scores,
            'monthly_activity': monthly_activity,
        })

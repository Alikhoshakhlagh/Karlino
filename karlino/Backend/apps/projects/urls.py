from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    MilestoneListCreateAPIView,
    MilestoneDetailAPIView,
    MilestoneDeliverAPIView,
    MilestoneApproveAPIView,
    MilestoneRejectAPIView,
    ProjectViewSet,
    PendingProjectsAPIView,
)

from ..bids.views import (
    CreateOrUpdateBidAPIView,
    ProjectBidListAPIView,
    AcceptBidAPIView,
    MyBidsAPIView,
    IncomingBidsAPIView,
    ExpertPendingBidsAPIView,
    ScoreBidAPIView,
    BidMessageAPIView,
)

router = DefaultRouter()
router.register(
    r'',
    ProjectViewSet,
    basename='projects',
)

urlpatterns = [

    # Expert
    path(
        'expert/bids/',
        ExpertPendingBidsAPIView.as_view(),
        name='expert-pending-bids',
    ),

    path(
        'expert/pending/',
        PendingProjectsAPIView.as_view(),
        name='expert-pending-projects',
    ),

    # Tender / Bids
    path(
        '<uuid:project_id>/bid/',
        CreateOrUpdateBidAPIView.as_view(),
        name='project-bid',
    ),

    path(
        '<uuid:project_id>/bids/',
        ProjectBidListAPIView.as_view(),
        name='project-bids',
    ),

    path(
        "<uuid:project_id>/bids/<uuid:bid_id>/accept/",
        AcceptBidAPIView.as_view(),
        name="accept-bid",
    ),

    path(
        '<uuid:project_id>/bids/<uuid:bid_id>/score/',
        ScoreBidAPIView.as_view(),
        name='score-bid',
    ),

    path(
        '<uuid:project_id>/bids/<uuid:bid_id>/message/',
        BidMessageAPIView.as_view(),
        name='bid-message',
    ),

    # Milestones
    path(
        '<uuid:project_id>/milestones/',
        MilestoneListCreateAPIView.as_view(),
        name='milestones',
    ),

    path(
        '<uuid:project_id>/milestones/<uuid:milestone_id>/',
        MilestoneDetailAPIView.as_view(),
        name='milestone-detail',
    ),

    path(
        '<uuid:project_id>/milestones/<uuid:milestone_id>/deliver/',
        MilestoneDeliverAPIView.as_view(),
        name='milestone-deliver',
    ),

    path(
        '<uuid:project_id>/milestones/<uuid:milestone_id>/approve/',
        MilestoneApproveAPIView.as_view(),
        name='milestone-approve',
    ),

    path(
        '<uuid:project_id>/milestones/<uuid:milestone_id>/reject/',
        MilestoneRejectAPIView.as_view(),
        name='milestone-reject',
    ),

    path(
        'my-bids/',
        MyBidsAPIView.as_view(),
        name='my-bids',
    ),

    path(
        'incoming-bids/',
        IncomingBidsAPIView.as_view(),
        name='incoming-bids',
    ),

    # Project ViewSet
    path(
        '',
        include(router.urls),
    ),
]
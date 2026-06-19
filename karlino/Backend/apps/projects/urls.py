from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    ProjectViewSet,
    PendingProjectsAPIView,
)

from ..bids.views import (
    CreateOrUpdateBidAPIView,
    ProjectBidListAPIView,
    AcceptBidAPIView,
    MyBidsAPIView,
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
        'my-bids/',
        MyBidsAPIView.as_view(),
        name='my-bids',
    ),

    # Project ViewSet
    path(
        '',
        include(router.urls),
    ),
]
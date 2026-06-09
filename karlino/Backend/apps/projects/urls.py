from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ProjectViewSet, PendingProjectsAPIView

router = DefaultRouter()
router.register(r"", ProjectViewSet, basename="projects")

urlpatterns = [
    path('expert/pending/',
         PendingProjectsAPIView.as_view(),
         name='expert-pending-projects'
         ),
    path("", include(router.urls)),
]
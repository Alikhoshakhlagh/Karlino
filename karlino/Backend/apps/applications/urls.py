from django.urls import path

from .views import (
    MyApplicationsAPIView,
    IncomingApplicationsAPIView,
    ApplicationAcceptAPIView,
    ApplicationRejectAPIView,
)

urlpatterns = [
    path('me/', MyApplicationsAPIView.as_view()),
    path('incoming/', IncomingApplicationsAPIView.as_view()),

    path(
        '<uuid:application_id>/accept/',
        ApplicationAcceptAPIView.as_view(),
        name='application-accept',
    ),

    path(
        '<uuid:application_id>/reject/',
        ApplicationRejectAPIView.as_view(),
        name='application-reject',
    ),
]
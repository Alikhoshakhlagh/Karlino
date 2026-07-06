from django.urls import path

from .views import (
    MyResumeAPIView,
    ResumeExperienceCreateAPIView,
    ResumeExperienceDetailAPIView,
)

urlpatterns = [
    path('', MyResumeAPIView.as_view(), name='my_resume',),

    path(
        'experiences/',
        ResumeExperienceCreateAPIView.as_view(),
        name='resume_experience_create',
    ),

    path(
        'experiences/<uuid:experience_id>/',
        ResumeExperienceDetailAPIView.as_view(),
        name='resume_experience_detail',
    ),
]

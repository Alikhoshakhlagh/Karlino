from django.urls import path

from .views import MyApplicationsAPIView, IncomingApplicationsAPIView

urlpatterns = [
    path('me/', MyApplicationsAPIView.as_view()),
    path('incoming/', IncomingApplicationsAPIView.as_view()),
]
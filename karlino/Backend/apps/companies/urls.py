from django.urls import path
from .views import MyCompanyAPIView

urlpatterns = [
    path("", MyCompanyAPIView.as_view()),
]
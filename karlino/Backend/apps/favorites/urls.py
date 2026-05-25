from django.urls import path

from .views import FavoriteListAPIView, FavoriteToggleAPIView

urlpatterns = [
    path('', FavoriteListAPIView.as_view()),
    path('<uuid:pk>/toggle/', FavoriteToggleAPIView.as_view()),
]
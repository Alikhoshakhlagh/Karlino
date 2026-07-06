from django.urls import path

from .views import (
    RegisterAPIView,
    ProfileAPIView,
    DashboardAPIView,
    SessionTokenObtainPairView,
    SessionTokenRefreshView,
    ChangePasswordAPIView,
    SessionListAPIView,
    SessionRevokeAPIView,
    ProfileChartsAPIView
)
from ..accounts.views import ResetPasswordView

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register',),
    path('login/', SessionTokenObtainPairView.as_view(), name='login',),
    path('token/refresh/', SessionTokenRefreshView.as_view(), name='token_refresh',),

    path('resetpassword/', ResetPasswordView.as_view(), name='reset_password',),
    path('change-password/', ChangePasswordAPIView.as_view(), name='change_password',),

    path('profile/', ProfileAPIView.as_view(), name='profile'),
    path('profile/charts/', ProfileChartsAPIView.as_view(), name='profile_charts',),

    path('dashboard/', DashboardAPIView.as_view(), name='dashboard',),

    path('sessions/', SessionListAPIView.as_view(), name='sessions',),
    path(
        'sessions/<uuid:session_id>/revoke/',
        SessionRevokeAPIView.as_view(),
        name='session_revoke',
    ),
]
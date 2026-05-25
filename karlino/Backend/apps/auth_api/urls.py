from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import (
    RegisterAPIView,
    ProfileAPIView,
)
from ..accounts.views import ResetPasswordView

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register',),
    path('login/', TokenObtainPairView.as_view(), name='login',),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh',),

    path('resetpassword/', ResetPasswordView.as_view(), name='reset_password',),

    path('profile/', ProfileAPIView.as_view(), name='profile'),
]
from rest_framework.routers import DefaultRouter

from .views import SkillViewSet


router = DefaultRouter()

router.register('', SkillViewSet, basename='skills')

urlpatterns = router.urls
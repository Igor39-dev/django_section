from django.urls import path
from apps.videos.views import VideoViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'v1/videos', VideoViewSet, basename='video')

urlpatterns = router.urls

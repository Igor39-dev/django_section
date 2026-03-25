from django.urls import path
from apps.videos.views import VideoViewSet

video_list = VideoViewSet.as_view({"get": "list"})
video_detail = VideoViewSet.as_view({"get": "retrieve"})
video_likes = VideoViewSet.as_view({"post": "likes", "delete": "likes"})
video_ids = VideoViewSet.as_view({"get": "ids"})
video_statistics_subquery = VideoViewSet.as_view({"get": "statistics_subquery"})
video_statistics_group = VideoViewSet.as_view({"get": "statistics_group_by"})


urlpatterns = [
    path("v1/videos/", video_list),
    path("v1/videos/<int:pk>/", video_detail),
    path("v1/videos/<int:pk>/likes/", video_likes),
    path("v1/videos/ids/", video_ids),
    path("v1/videos/statistics-subquery/", video_statistics_subquery),
    path("v1/videos/statistics-group-by/", video_statistics_group),
]

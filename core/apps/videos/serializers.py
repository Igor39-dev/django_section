from rest_framework import serializers

from apps.users.models import AppUser
from apps.videos.models import Video, VideoFile
from apps.users.serializers import AppUserPreviewSerializer

class VideoRetrieveFileSerializer(serializers.ModelSerializer):

    class Meta:
        model = VideoFile
        fields = ("file", "quality",)


class VideoRetrieveSerializer(serializers.ModelSerializer):

    owner = AppUserPreviewSerializer()
    files = VideoRetrieveFileSerializer(many=True)

    class Meta:
        model = Video
        fields = ("id", "owner", "files", "name", "total_likes", "created_at",)


class StatisticsSerializer(serializers.Serializer):

    username = serializers.CharField()
    likes_sum = serializers.IntegerField()

    class Meta:
        model = AppUser
        fields = ("username", "likes_sum")

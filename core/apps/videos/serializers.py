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


class VideoFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoFile
        fields = ("id", "file", "quality")
        read_only_fields = ("id",)

class VideoSerializer(serializers.ModelSerializer):
    files = VideoFileSerializer(many=True, required=False)
    owner_username = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = Video
        fields = ("id", "owner_username", "owner", "name", "is_published", "total_likes", "created_at", "files")
        read_only_fields = ("id", "total_likes", "created_at")

    def create(self, validated_data):
        files_data = validated_data.pop("files", [])
        video = Video.objects.create(**validated_data)
        for file_data in files_data:
            VideoFile.objects.create(video=video, **file_data)
        return video

    def update(self, instance, validated_data):
        files_data = validated_data.pop("files", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if files_data is not None:
            instance.files.all().delete()
            for file_data in files_data:
                VideoFile.objects.create(video=instance, **file_data)
        return instance

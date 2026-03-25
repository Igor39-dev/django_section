from django.db.models import OuterRef, Sum, Q

from rest_framework import mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.users.models import AppUser
from apps.videos.models import Video
from apps.videos.serializers import VideoRetrieveSerializer, StatisticsSerializer, VideoSerializer

from apps.videos.services.likes import LikeSetter


class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all().prefetch_related("files")
    serializer_class = VideoSerializer

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user

        if user.is_staff:
            return qs
        if user.is_authenticated:
            return qs.filter(Q(is_published=True) | Q(owner=user))
        return qs.filter(is_published=True)
    
    '''POST /v1/videos/{id}/likes/
        DELETE /v1/videos/{id}/likes/'''
    @action(
        methods=["POST", "DELETE"],
        detail=True,
        permission_classes=[permissions.IsAuthenticated],
    )
    def likes(self, request, pk=None):

        video = self.get_object()
        handler = LikeSetter(user=request.user, video=video,)

        if request.method == "POST":
            handler.like()
            return Response(status=status.HTTP_201_CREATED)

        if request.method == "DELETE":
            handler.unlike()
            return Response(status=status.HTTP_204_NO_CONTENT)


    '''GET /v1/videos/ids/'''
    @action(
        methods=["GET"],
        detail=False,
        permission_classes=[permissions.IsAdminUser],
    )
    def ids(self, request):

        ids = Video.objects.published().values_list("id", flat=True,)
        return Response(ids)


    '''GET /v1/videos/statistics-subquery/'''
    @action(
        methods=["GET"],
        detail=False,
        url_path="statistics-subquery",
        permission_classes=[permissions.IsAdminUser],
    )
    def statistics_subquery(self, request):

        likes_sum = (
            Video.objects.published()
            .filter(owner=OuterRef("pk"))
            .values("owner")
            .annotate(
                likes_sum=Sum("total_likes")
            )
            .values("likes_sum")
        )

        users = (
            AppUser.objects
            .values("username")
            .annotate(likes_sum=likes_sum)
            .order_by("-likes_sum")
        )

        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data)
    

    '''GET /v1/videos/statistics-group-by/'''
    @action(
        methods=["GET"],
        detail=False,
        url_path="statistics-group-by",
        permission_classes=[permissions.IsAdminUser],
    )
    def statistics_group_by(self, request):

        videos = Video.objects.statistics()
        serializer = self.get_serializer(videos, many=True)
        return Response(serializer.data)
    
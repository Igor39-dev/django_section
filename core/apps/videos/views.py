from django.db.models import OuterRef, Sum

from rest_framework import mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.users.models import AppUser
from apps.videos.models import Video
from apps.videos.serializers import VideoRetrieveSerializer, StatisticsSerializer

from apps.videos.services.likes import LikeSetter


class VideoViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):

    queryset = Video.objects.all()

    def get_queryset(self):
        qs = Video.objects.prefetch_related("files").order_by("-created_at")

        if self.action in ("likes", "ids"):
            return Video.objects.published()
        if self.request.user.is_staff:
            return qs
        return qs.published(user=self.request.user)
    
    def get_serializer_class(self):

        if self.action in ("list", "retrieve"):
            return VideoRetrieveSerializer
        if self.action in ("statistics_subquery", "statistics_group_by",):
            return StatisticsSerializer
        return VideoRetrieveSerializer
    
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
    
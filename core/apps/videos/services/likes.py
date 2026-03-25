from django.db import IntegrityError, transaction
from django.db.models import F

from apps.videos.models import Like, Video


class LikeSetter:

    def __init__(self, user, video: Video):
        self.user = user
        self.video = video

    @transaction.atomic
    def like(self):
        '''POST like'''
        if not self.video.is_published:
            return
        try:
            Like.objects.create(user=self.user, video=self.video)
            Video.objects.filter(id=self.video.id).update(total_likes=F("total_likes") + 1)
        except IntegrityError:
            pass


    @transaction.atomic
    def unlike(self):
        '''DELETE like'''
        if not self.video.is_published:
            return
        deleted, _ = Like.objects.filter(user=self.user, video=self.video).delete()

        if deleted:
            Video.objects.filter(id=self.video.id).update(total_likes=F("total_likes") - 1)
            
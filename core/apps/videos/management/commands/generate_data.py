import random

from django.core.management.base import BaseCommand
from django.db import transaction

from apps.users.models import AppUser
from apps.videos.models import Video


class Command(BaseCommand):

    help = "Generate users and videos"
    def handle(self, *args, **kwargs):
        self.stdout.write("Creating users...")
        users = [
            AppUser(username=f"user_{i}")
            for i in range(10000)
        ]

        AppUser.objects.bulk_create(users)
        self.stdout.write("Users created")
        users = list(AppUser.objects.all())
        self.stdout.write("Creating videos...")
        videos = []

        for i in range(100000):
            videos.append(
                Video(
                    owner=random.choice(users),
                    name=f"video_{i}",
                    is_published=True,
                    total_likes=random.randint(0, 100),
                )
            )

            if len(videos) == 5000:
                Video.objects.bulk_create(videos)
                videos.clear()
                self.stdout.write(f"{i} videos created")

        if videos:
            Video.objects.bulk_create(videos)

        self.stdout.write("Done")
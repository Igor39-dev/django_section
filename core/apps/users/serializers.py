from rest_framework import serializers
from apps.users.models import AppUser


class AppUserPreviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = AppUser
        fields = ("username",)

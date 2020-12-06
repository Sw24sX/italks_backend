from rest_framework import serializers

from ..models import FavouritesVideos


class FavoriteVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavouritesVideos
        fields = "__all__"

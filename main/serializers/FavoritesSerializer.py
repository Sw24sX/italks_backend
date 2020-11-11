from rest_framework import serializers

from ..models import Favourites


class FavoriteVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favourites
        fields = "__all__"

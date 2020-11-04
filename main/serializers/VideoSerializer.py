from rest_framework import serializers

from ..models import Video, Category


class VideoSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='name', read_only=True)
    subcategory = serializers.SlugRelatedField(slug_field='name', many=True, read_only=True)


    class Meta:
        model = Video
        fields = "__all__"


class SearchResultSerializer(serializers.Serializer):
    result = VideoSerializer(many=True)

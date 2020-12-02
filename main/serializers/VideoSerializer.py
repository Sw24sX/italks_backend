from rest_framework import serializers

from ..models import Video, Category, Author


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('name', 'src')


class VideoSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='name', many=True, read_only=True)
    subcategory = serializers.SlugRelatedField(slug_field='name', many=True, read_only=True)
    conference = serializers.SlugRelatedField(slug_field='name', read_only=True)
    resource = serializers.SlugRelatedField(slug_field='name', read_only=True)
    author = AuthorSerializer()


    class Meta:
        model = Video
        fields = "__all__"


class SearchResultSerializer(serializers.Serializer):
    result = VideoSerializer(many=True)

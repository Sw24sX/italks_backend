from rest_framework import serializers

from ..models import Video, Category, Author, Resource
from ..serializers.CategorySerializer import CategorySerializer, SubcategorySerializer


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('name', 'src')


class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = ('name', 'src')


class VideoSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=True)
    subcategory = SubcategorySerializer(many=True)
    conference = serializers.SlugRelatedField(slug_field='name', read_only=True)
    resource = ResourceSerializer()
    author = AuthorSerializer()


    class Meta:
        model = Video
        fields = "__all__"


class SearchResultSerializer(serializers.Serializer):
    result = VideoSerializer(many=True)

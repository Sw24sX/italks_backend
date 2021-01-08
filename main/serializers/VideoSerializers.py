from rest_framework import serializers

from ..models import Video, Category, Author, Resource, FavouritesVideos, LastWatchVideo, ProgressVideoWatch
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

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['is_favorite'] = False
        if 'user' in self.context:
            user = self.context['user']
            time = 0
            if not user.is_anonymous:
                representation['is_favorite'] = FavouritesVideos.objects.filter(user=user, video=instance).exists()

                time = ProgressVideoWatch.objects \
                    .filter(user=user, video=instance) \
                    .values_list('time', flat=True) \
                    .first()
                if time is None:
                    time = 0
            representation['time'] = time

        return representation

    class Meta:
        model = Video
        fields = "__all__"


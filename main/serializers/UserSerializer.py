from rest_framework import serializers
from ..models import UserSettings, User, ProgressVideoWatch, Video, LastWatchVideo
from ..serializers.VideoSerializers import VideoSerializer


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        settings, _ = UserSettings.objects.get_or_create(user=instance)
        representation['dark_theme'] = settings.dark_theme
        representation['last_video'] = None

        if 'last_video' in self.context:
            video = self.context['last_video']
            time = ProgressVideoWatch.objects\
                .filter(user=instance, video=video)\
                .values_list('time', flat=True)\
                .first()
            representation['last_video'] = VideoSerializer(video, context={'user': instance}).data
        return representation


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class UserSettingsSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = UserSettings
        fields = ('user', 'notifications', 'dark_theme', 'as_device')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['email_is_change'] = 'email_is_change' in self.context and self.context['email_is_change']
        return representation

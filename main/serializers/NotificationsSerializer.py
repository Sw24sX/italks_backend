from rest_framework import serializers
from ..models import UserSettings, User, Notifications
from ..serializers.VideoSerializers import VideoSerializer


class NotificationsSerializer(serializers.ModelSerializer):
    user_id = serializers.SlugRelatedField(slug_field='id', read_only=True, source='user')
    video = VideoSerializer(many=False)

    class Meta:
        model = Notifications
        fields = ('user_id', 'video', 'date',)

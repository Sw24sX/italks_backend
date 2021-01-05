from rest_framework import serializers
from ..models import UserSettings, User
#from ..serializers.VideoSerializer import VideoSerializer


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['last_video'] = None
        #if 'last_video' in self.context:
            #representation['last_video'] = VideoSerializer(self.context['last_video'], context=instance)


class UserDataSettingsSerializer(serializers.Serializer):
    username = serializers.CharField()
    old_password = serializers.CharField()
    new_password = serializers.CharField()

    def create(self, validated_data):
        return validated_data

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.username = validated_data.get('username', instance.username)
        instance.new_password = validated_data.get('password', instance.new_password)
        return instance


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

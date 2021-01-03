from rest_framework import serializers
from ..models import UserSettings, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')


class UserSettingsSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = UserSettings
        fields = ('user', 'notifications', 'dark_theme', 'as_device')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['email_is_change'] = 'email_is_change' in self.context and self.context['email_is_change']
        return representation

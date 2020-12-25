from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions as django_exceptions
from django.db import IntegrityError, transaction
from djoser.conf import settings
from rest_framework import serializers
from djoser.serializers import UserCreateSerializer

from ..models import Author

User = get_user_model()


class CustomUserCreateSerializer(UserCreateSerializer):
    def validate(self, attrs):
        user = User(**attrs)
        password = attrs.get("password")

        try:
            validate_password(password, user)
        except django_exceptions.ValidationError as e:
            serializer_error = serializers.as_serializer_error(e)
            raise serializers.ValidationError(
                {"password": serializer_error["non_field_errors"]}
            )

        return attrs


class TestSerializer(serializers.Serializer):

    def to_representation(self, instance):
        request = self.context['request']
        representation = super().to_representation(instance)
        representation['IsFavorite'] = True
        user = request.user
        author = Author.objects.get(pk=1)
        representation['user'] = AuthorSerializer(author).data
        if user.is_active:
            representation['IsActive'] = True
        else:
            representation['IsActive'] = False
        return representation


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('name', 'src')

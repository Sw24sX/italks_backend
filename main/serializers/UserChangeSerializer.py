from rest_framework import serializers
from django.contrib.auth.models import User


class UserAuthSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100)


class UserChangeSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=150)
    email = serializers.CharField(max_length=150)


class UserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.CharField(max_length=150)

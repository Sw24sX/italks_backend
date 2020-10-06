from rest_framework.response import Response
from rest_framework.views import APIView

from django.contrib.auth.models import User
from django.contrib import auth

from ..serializers.UserSerializer import UserAuthSerializer, UserChangeSerializer, UserSerializer
from .. import validators


class UserAuthView(APIView):
    """Авторизация пользователя"""
    def post(self, request):
        serializer = UserAuthSerializer(data=request.data)
        serializer.is_valid()
        user = auth.authenticate(username=serializer.data['username'], password=serializer.data['password'])
        auth.login(request, user)
        return Response(serializer.data, status=201)

    """Выход"""
    def get(self, request):
        if auth.get_user(request).is_authenticated:
            auth.logout(request)
            return Response({}, status=201)

        return Response({}, status=400)


class UserDataView(APIView):
    """Изменение данных пользователя"""
    def put(self, request):
        # todo изменение данных пользователя
        return Response(status=201)

    """Создание пользователя"""
    def post(self, request):
        serializer = UserChangeSerializer(data=request.data)
        serializer.is_valid()
        username = serializer.data['username']
        password = serializer.data['password']
        email = serializer.data['email']

        username_errors = validators.username_validator(username)
        password_errors = validators.password_validator(password)
        email_errors = validators.email_validator(email)

        if len(username_errors) + len(password_errors) + len(email_errors) == 0:
            User.objects.create_user(
                username=username,
                password=password,
                email=email
            )
            return Response(serializer.data, status=201)
        args = {
            'username': username_errors,
            'password': password_errors,
            'email': email_errors
        }
        return Response(args, status=400)


class UserView(APIView):
    """Получить данные о пользователе"""
    def get(self, request):
        if not auth.get_user(request).is_authenticated:
            return Response({'user': "anonimus"}, status=201)
        user = auth.get_user(request)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=201)



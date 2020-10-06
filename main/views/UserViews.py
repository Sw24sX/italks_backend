from rest_framework.response import Response
from rest_framework.views import APIView

from django.contrib.auth.models import User
from django.contrib import auth

from ..serializers.UserSerializer import UserAuthSerializer, UserSerializer


class UserAuthView(APIView):
    """Изменить статус авторизованности пользователя"""
    def post(self, request):
        if auth.get_user(request).is_authenticated:
            auth.logout(request)
            return Response({}, status=201)

        serializer = UserAuthSerializer(data=request.data)
        serializer.is_valid()
        user = auth.authenticate(username=serializer.data['username'], password=serializer.data['password'])
        auth.login(request, user)
        return Response(serializer.data, status=201)


class UserDataView(APIView):
    """Изменение данных пользователя"""
    def put(self, request):
        # todo изменение данных пользователя
        return Response(status=201)

    """Создание пользователя"""
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid()
        User.objects.create_user(
            username=serializer.data['username'],
            password=serializer.data['password'],
            email=serializer.data['email']
        )
        #todo create validators
        return Response(serializer.data, status=201)


class UserView(APIView):
    """Получить данные о пользователе"""
    def get(self, request):
        if not auth.get_user(request).is_authenticated:
            return Response({'user': "anonimus"}, status=201)
        user = auth.get_user(request)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=201)



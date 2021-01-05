import re
from datetime import date

from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework import permissions

from django.contrib.auth import password_validation
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError

from ..models import UserSettings, LastWatchVideo, Video
from ..serializers.UserSerializer import UserSettingsSerializer,  UserInfoSerializer


class CheckToken(APIView):
    """Проверка на актуальность токена + информация о пользователе"""

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        video_id = LastWatchVideo.objects.filter(user=request.user)\
            .values_list('id', flat=True)\
            .first()
        context = {}
        if video_id is not None:
            video = Video.objects.get(pk=video_id)
            context['last_video'] = video
        LastWatchVideo
        serialized = UserInfoSerializer(request.user, context=context)
        return Response(serialized.data, status=200)


class UserSettingsInput:
    username: str = None
    new_password: str = None
    old_password: str = None
    request: Request = None
    errors: dict = {}

    def __init__(self, request: Request):
        data = request.data

        if 'username' in data:
            self.username = data['username']
        if 'new_password' in data:
            self.new_password = data['new_password']
        if 'old_password' in data:
            self.old_password = data['old_password']
        self.request = request

    def update_without_save_user_data(self) -> bool:
        user = self.request.user
        if self._username_is_change():
            reg = re.compile('[^a-z0-9_]')
            if len(reg.sub('', self.username)) != len(self.username):
                self.errors['username'] = 'Имя не может содержать спецсимволы'
            else:
                user.username = self.username

        if self._new_password_is_change():
            if self._old_password_is_correct():
                try:
                    password_validation.validate_password(self.new_password, user=self.request.user)
                except ValidationError as err:
                    self.errors['new_password'] = err.messages[0]
                else:
                    user.set_password(self.new_password)
            else:
                self.errors['old_password'] = 'Старый пароль не верный'

        return len(self.errors) == 0

    def _username_is_change(self) -> bool:
        return self.username is not None and self.request.user.username != self.username

    def _old_password_is_correct(self) -> bool:
        return self.old_password is not None and self.request.user.check_password(self.old_password)

    def _new_password_is_change(self) -> bool:
        return self.new_password is not None and not self.request.user.check_password(self.new_password)


class Settings(APIView):
    """Получениие данных настроек пользователя"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request):
        settings, created = UserSettings.objects.get_or_create(user=request.user)
        serialized = UserSettingsSerializer(settings)
        return Response(serialized.data, status=200)


class UserSettingsView(APIView):
    """Сохранение изменений данных пользователя"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request: Request):
        try:
            user_settings = UserSettingsInput(request)
        except ValueError:
            return Response(status=400)

        updated = user_settings.update_without_save_user_data()
        if not updated:
            data = {
                'info_user': {'username': request.user.username},
                'errors': user_settings.errors,
            }
            return Response(data, status=400)

        data = {
            'info_user': {'username': request.user.username},
        }
        return Response(data, status=200)


class OtherSettingsView(APIView):
    """Изменение всех флагов"""

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request: Request):
        values_for_update = {}
        settings, created = UserSettings.objects.get_or_create(user=request.user)

        notifications = request.query_params.get('notifications', None)
        if notifications is not None:
            values_for_update['notifications'] = self._str_to_bool(notifications)

        dark_theme = request.query_params.get('dark_theme', None)
        if dark_theme is not None:
            dark_theme = self._str_to_bool(dark_theme)
            values_for_update['dark_theme'] = dark_theme

        as_device = request.query_params.get('as_device', None)
        if as_device is not None:
            as_device = self._str_to_bool(as_device)

            values_for_update['as_device'] = as_device

        if len(values_for_update) != 0:
            settings, __ = UserSettings.objects.update_or_create(user=request.user, defaults=values_for_update)

        serialized = UserSettingsSerializer(settings)
        return Response(serialized.data, status=200)

    def _str_to_bool(self, value: str):
        return value.lower() in ('yes', 'true', '1')


class NotificationsSettingsView(APIView):
    '''Изменение флага "получать уведомления"'''

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request: Request, is_notification: int):
        _, __ = UserSettings.objects.update_or_create(user=request.user, defaults={'notifications': bool(is_notification)})
        return Response(status=200)


class DarkThemeSettingsView(APIView):
    '''Изменение флага "темная тема"'''

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request: Request, is_dark_theme: int):
        if not bool(is_dark_theme):
            values_for_update = {
                'dark_theme': False,
                'as_device': False
             }
            _, __ = UserSettings.objects.update_or_create(user=request.user, defaults=values_for_update)
        else:
            _, __ = UserSettings.objects.update_or_create(user=request.user, defaults={'dark_theme': True})
        return Response(status=200)


class AsDeviceSettingsView(APIView):
    '''Изменение флага "как на устройстве"'''

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request: Request, is_as_device: int):
        user_settings, created = UserSettings.objects.get_or_create(user=request.user)
        if not user_settings.dark_theme:
            return Response(status=400)

        user_settings.as_device = bool(is_as_device)
        return Response(status=200)

import re
from datetime import date

from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework import permissions

from django.contrib.auth import password_validation
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError

from ..models import UserSettings
from ..serializers.UserSerializer import UserSettingsSerializer


class CheckToken(APIView):
    """Проверка на актуальность токена"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response(status=201)


class UserSettingsInput:
    username: str
    password: str
    email: str
    request: Request

    def __init__(self, request: Request):
        self.username = request.query_params.get('username', None)
        self.password = request.query_params.get('password', None)
        self.email = request.query_params.get('email', None)
        self.request = request

        if None in [self.username, self.password, self.email]:
            raise ValueError

    def update_user_data(self) -> dict:
        errors = {}
        user = self.request.user
        if self._username_is_change():
            reg = re.compile('[^a-z0-9_]')
            if len(reg.sub('', self.username)) != len(self.username):
                errors['username'] = ['Имя не может содержать спецсимволы']
            else:
                user.username = self.username
        if self.email_is_change():
            errors_messages = self._email_validation()
            if errors_messages is not None:
                errors['email'] = errors_messages
            else:
                user.email = self.email
        if self._password_is_change():
            try:
                password_validation.validate_password(self.password, user=self.request.user)
            except ValidationError as err:
                errors['password'] = err.messages
            else:
                user.set_password(self.password)
        if len(errors) == 0:
            user.save()
        return errors

    def email_is_change(self) -> bool:
        return self.email != self.request.user.email

    def _email_validation(self):
        email_validator = EmailValidator()
        try:
            email_validator(self.email)
        except ValidationError as error:
            return error.messages

    def _username_is_change(self) -> bool:
        return self.request.user.username != self.username

    def _password_is_change(self) -> bool:
        return not self.request.user.check_password(self.password)


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

        if user_settings.email_is_change():
            # todo send email
            pass

        errors = user_settings.update_user_data()
        if len(errors) != 0:
            return Response(errors, status=200)

        settings = UserSettings.objects.filter(user=request.user).first()
        if settings is not None:
            return Response(status=400)

        serialized = UserSettingsSerializer(settings)
        return Response(serialized.data, status=200)


class OtherSettingsView(APIView):
    """todo"""

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
            if not dark_theme:
                values_for_update['as_device'] = False

        as_device = request.query_params.get('as_device', None)
        if as_device is not None:
            as_device = self._str_to_bool(as_device)
            if as_device and ((dark_theme is not None and not dark_theme) or not settings.dark_theme):
                return Response(status=400)

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

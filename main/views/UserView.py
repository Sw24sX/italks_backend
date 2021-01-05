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
from ..serializers.UserSerializer import UserSettingsSerializer, UserSerializer, UserDataSettingsSerializer


class CheckToken(APIView):
    """Проверка на актуальность токена + информация о пользователе"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):

        return Response(status=200)


class UserSettingsInput:
    username: str = None
    new_password: str = None
    old_password: str = None
    request: Request = None

    def __init__(self, request: Request):
        data = request.data

        if 'username' in data:
            self.username = data['username']
        if 'new_password' in data:
            self.new_password = data['new_password']
        if 'old_password' in data:
            self.old_password = data['old_password']
        self.request = request

        #if None in [self.username, self.password, self.email]:
        #    raise ValueError

    def update_user_data(self) -> dict:
        errors = {}
        user = self.request.user
        if self._username_is_change():
            reg = re.compile('[^a-z0-9_]')
            if len(reg.sub('', self.username)) != len(self.username):
                errors['username'] = 'Имя не может содержать спецсимволы'
            else:
                user.username = self.username
        #if self.email_is_change():
        #    errors_messages = self._email_validation()
        #    if errors_messages is not None:
        #        errors['email'] = errors_messages
        #    else:
        #        user.email = self.email
        if self._new_password_is_change():
            if self._old_password_is_correct():
                try:
                    password_validation.validate_password(self.new_password, user=self.request.user)
                except ValidationError as err:
                    errors['password'] = err.messages[0]
                else:
                    user.set_password(self.new_password)
            else:
                errors['password'] = 'Старый пароль не верный'
        if len(errors) == 0:
            user.save()
        return errors

    #def email_is_change(self) -> bool:
    #    return self.email is not None and self.email != self.request.user.email

    def _email_validation(self):
        email_validator = EmailValidator()
        try:
            #email_validator(self.email)
            pass
        except ValidationError as error:
            return error.messages

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

        #if user_settings.email_is_change():
        #    # todo send email
        #    pass

        errors = user_settings.update_user_data()
        if len(errors) != 0:
            data = {
                'info_user': {'username': request.user.username},
                'errors': errors,
            }
            return Response(data, status=400)

        #settings = UserSettings.objects.filter(user=request.user).first()
        #if settings is not None:
        #    return Response(status=400)

        #serialized = UserSettingsSerializer(settings)
        #serialized = UserSerializer(request.user)
        data = {
            'info_user': {'username': request.user.username},
        }
        return Response(data, status=200)


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
            #if not dark_theme:
            #    values_for_update['as_device'] = False

        as_device = request.query_params.get('as_device', None)
        if as_device is not None:
            as_device = self._str_to_bool(as_device)
            #if as_device and ((dark_theme is not None and not dark_theme) or not settings.dark_theme):
            #    return Response(status=400)

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

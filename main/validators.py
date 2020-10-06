import re
import emoji

from django.contrib.auth.models import User
from django.contrib.auth import password_validation, validators
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator


def username_validator(username: str) -> list:
    result = []
    username = username.lower()
    users = User.objects.all()
    other_users = list(filter(lambda x: x.username == username, users))

    if len(other_users) != 0:
        result.append('Логин уже занят')
    if len(username) < 1:
        result.append('Введите логин')
    if len(username) < 3:
        result.append('Минимальная длинна логина - 3 символа')
    if len(username) > 0 and not username[0].isalpha():
        result.append('Логин должен начинаться с буквы')

    reg = re.compile('[^a-z0-9_]')
    if len(reg.sub('', username)) != len(username):
        result.append('Логин содержит запрещенные символы')
    return result


def password_validator(password: str) -> list:
    result = []
    try:
        password_validation.validate_password(password)
    except ValidationError as error:
        result = error.messages
    if bool(emoji.get_emoji_regexp().search(password)):
        result.append('Пароль содержит запрещенные символы')
    return result


def email_validator(email: str) -> list:
    result = []
    if len(email) != 0:
        try:
            email_validator = EmailValidator()
            email_validator(email)
        except ValidationError as error:
            result = error.messages
        users = User.objects.filter(email=email)
        if len(users) != 0:
            result.append('Данный email уже привязан к другому аккаунту')
    else:
        result.append('Введите значение')
    return result

import re

from django.contrib.auth.models import User


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
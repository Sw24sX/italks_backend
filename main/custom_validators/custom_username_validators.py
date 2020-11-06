from django.utils.translation import gettext_lazy as _
from django.core import validators


def custom_username_validators(value):
    pass


class CustomUnicodeUsernameValidator(validators.RegexValidator):
    regex = r'^[\w.@+-]+\Z'
    message = _(
        'Имя не может содержать спецсимволы'
    )
    flags = 0


from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError, FieldDoesNotExist
from django.utils.translation import gettext as _, ngettext
from difflib import SequenceMatcher
import re


class CustomMinimumLengthValidator(password_validation.MinimumLengthValidator):
    def validate(self, password, user=None):
        if len(password) < self.min_length:
            raise ValidationError(
                ngettext(
                    "Пароль не может быть менее %(min_length)d символов",
                    "Пароль не может быть менее %(min_length)d символов",
                    self.min_length
                ),
                code='password_too_short',
                params={'min_length': self.min_length},
            )


class CustomCommonPasswordValidator(password_validation.CommonPasswordValidator):
    def validate(self, password, user=None):
        if password.lower().strip() in self.passwords:
            raise ValidationError(
                _("Этот пароль слишком распространен"),
                code='password_too_common',
            )


class CustomNumericPasswordValidator(password_validation.NumericPasswordValidator):
    def validate(self, password, user=None):
        if password.isdigit():
            raise ValidationError(
                _("Пароль не может состоять только из цифр"),
                code='password_entirely_numeric',
            )


class CustomUserAttributeSimilarityValidator(password_validation.UserAttributeSimilarityValidator):
    def validate(self, password, user=None):
        if not user:
            return

        for attribute_name in self.user_attributes:
            value = getattr(user, attribute_name, None)
            if not value or not isinstance(value, str):
                continue
            value_parts = re.split(r'\W+', value) + [value]
            for value_part in value_parts:
                if SequenceMatcher(a=password.lower(), b=value_part.lower()).quick_ratio() >= self.max_similarity:
                    try:
                        verbose_name = str(user._meta.get_field(attribute_name).verbose_name)
                    except FieldDoesNotExist:
                        verbose_name = attribute_name
                    raise ValidationError(
                        _("Пароль и %(verbose_name)s совпадают"),
                        code='password_too_similar',
                        params={'verbose_name': verbose_name},
                    )

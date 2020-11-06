from django.db import models
from .custom_validators.custom_username_validators import CustomUnicodeUsernameValidator
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    username_validator = CustomUnicodeUsernameValidator()

    username = models.CharField(
        _('username'),
        max_length=150,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )

    email = models.EmailField(_('email address'), blank=True, unique=True)

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    icon = models.TextField()
    objects = models.Manager()

    class Meta:
        db_table = "Category"

    def __str__(self):
        return self.name


class CategoryNames(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    objects = models.Manager()

    class Meta:
        db_table = "Category names"

    def __str__(self):
        return self.name


class Subcategory(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategory')
    objects = models.Manager()

    class Meta:
        db_table = "Subcategory"
        unique_together = ('name', 'category')

    def __str__(self):
        return "{}: {}".format(self.category, self.name)


class SubcategoryNames(models.Model):
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    objects = models.Manager()

    class Meta:
        db_table = "Subcategory names"

    def __str__(self):
        return self.name


class Video(models.Model):
    name = models.CharField(max_length=100)
    src = models.CharField(max_length=30, unique=True)
    category = models.ManyToManyField(Category)
    subcategory = models.ManyToManyField(Subcategory)

    class Meta:
        db_table = "Video"
        # todo возможно есть ошибка в уникальности категории и подкатегории

    def __str__(self):
        return self.name

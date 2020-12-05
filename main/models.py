from datetime import datetime

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

    email = models.EmailField(_('email address'), blank=False, unique=True)

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    icon_base_64 = models.TextField()
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


class Resource(models.Model):
    name = models.CharField(max_length=100)
    src = models.TextField()

    class Meta:
        db_table = "Resource"

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=100)
    src = models.TextField()

    class Meta:
        db_table = "Author"

    def __str__(self):
        return self.name


class Video(models.Model):
    name = models.CharField(max_length=100)
    src = models.CharField(max_length=30) #todo (Временно для удобства разработки) unique=True
    category = models.ManyToManyField(Category)
    subcategory = models.ManyToManyField(Subcategory)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    duration = models.IntegerField(default=0)
    date = models.DateField(auto_now_add=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    #todo temp; добавить веса и сортировку по ним
    is_favorite = models.BooleanField(default=False)

    class Meta:
        db_table = "Video"
        # todo возможно есть ошибка в уникальности категории и подкатегории

    def __str__(self):
        return self.name


class Favourites(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='favorite_video')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = "Favorites"
        unique_together = ('video', 'user')


class UpcomingEvent(models.Model):
    name = models.CharField(max_length=150)
    data = models.DateField()
    url = models.TextField()
    image = models.ImageField(default='', upload_to='images/', blank=True)

    class Meta:
        db_table = "Events"
        unique_together = ('name', 'data')
        ordering = ['data']

from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    icon = models.ImageField(upload_to='icons/', blank=True)
    objects = models.Manager()

    class Meta:
        db_table = "Category"

    def __str__(self):
        return self.name


class Subcategory(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    objects = models.Manager()

    class Meta:
        db_table = "Subcategory"
        unique_together = ('name', 'category')

    def __str__(self):
        return "{}: {}".format(self.category, self.name)


class Video(models.Model):
    name = models.CharField(max_length=100)
    src = models.CharField(max_length=30, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ManyToManyField(Subcategory)

    class Meta:
        db_table = "Video"
        # todo возможно есть ошибка в уникальности категории и подкатегории

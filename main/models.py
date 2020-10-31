from django.db import models


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

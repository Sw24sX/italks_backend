# Generated by Django 3.1.2 on 2020-12-25 19:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0026_favoritessubcategory'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='video',
            name='is_favorite',
        ),
    ]
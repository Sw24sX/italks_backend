# Generated by Django 3.1.2 on 2020-10-31 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0016_auto_20201031_1803'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='search_name',
            field=models.CharField(default='', max_length=100),
        ),
    ]
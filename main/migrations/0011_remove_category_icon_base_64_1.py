# Generated by Django 3.1.2 on 2020-10-18 20:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_auto_20201019_0103'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='icon_base_64_1',
        ),
    ]
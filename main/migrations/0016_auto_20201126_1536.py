# Generated by Django 3.1.2 on 2020-11-26 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_auto_20201126_1536'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='date',
            field=models.DateField(auto_now_add=True),
        ),
    ]
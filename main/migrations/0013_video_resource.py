# Generated by Django 3.1.2 on 2020-11-25 19:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_resource'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='resource',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='main.resource'),
        ),
    ]

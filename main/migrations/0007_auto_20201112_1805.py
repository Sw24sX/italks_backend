# Generated by Django 3.1.2 on 2020-11-12 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_upcomingevent'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='upcomingevent',
            options={'ordering': ['data']},
        ),
        migrations.AlterField(
            model_name='upcomingevent',
            name='image',
            field=models.ImageField(blank=True, default='', upload_to='images/'),
        ),
    ]

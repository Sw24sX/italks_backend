# Generated by Django 3.1.2 on 2020-10-13 22:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='category',
            table='Category',
        ),
        migrations.AlterModelTable(
            name='subcategory',
            table='Subcategory',
        ),
    ]

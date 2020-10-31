# Generated by Django 3.1.2 on 2020-10-31 14:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0017_category_search_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='search_name',
        ),
        migrations.CreateModel(
            name='NameCategoryForSearch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.category')),
            ],
            options={
                'db_table': 'Category names',
            },
        ),
    ]

# Generated by Django 4.2.2 on 2023-06-19 12:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Тип')),
            ],
            options={
                'verbose_name': 'Тип',
                'verbose_name_plural': 'Типы',
            },
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Название аниме')),
                ('original_name', models.CharField(max_length=100, verbose_name='Оригинальное название')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='photos/', verbose_name='Изображение')),
                ('releases', models.CharField(max_length=100, verbose_name='Годы выпуска')),
                ('description', models.TextField(verbose_name='Описание')),
                ('age_limit', models.CharField(max_length=10, verbose_name='Возрастное ограничение')),
                ('genre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.category')),
            ],
            options={
                'verbose_name': 'Статья',
                'verbose_name_plural': 'Статьи',
            },
        ),
    ]

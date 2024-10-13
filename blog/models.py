from datetime import datetime

from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.urls import reverse


class Category(models.Model):
    title = models.CharField(max_length=50, verbose_name='Тип')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Тип'
        verbose_name_plural = 'Типы'


class Article(models.Model):
    title = models.CharField(max_length=50, verbose_name='Название аниме')
    original_name = models.CharField(max_length=100, verbose_name='Оригинальное название')
    photo = models.ImageField(upload_to='photos/', blank=True, null=True, verbose_name='Изображение')
    episodes = models.CharField(max_length=150, verbose_name='Кол-во сезонов, серий, фильмов', blank=True, null=True)
    genres = models.CharField(max_length=200, verbose_name='Жанры', blank=True, null=True)
    releases = models.CharField(max_length=100, verbose_name='Годы выпуска')
    description = models.TextField(verbose_name='Описание')
    age_limit = models.CharField(max_length=10, verbose_name='Возрастное ограничение')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания', blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения', blank=True, null=True)
    views = models.IntegerField(default=0, verbose_name='Просмотры', blank=True, null=True)
    video = models.CharField(max_length=500, verbose_name='Ссылка на видео', blank=True, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'


class Status(models.Model):
    title = models.CharField(max_length=255, verbose_name='Статус')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'


class Rank(models.Model):
    title = models.CharField(max_length=255, verbose_name='Звание')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Звание'
        verbose_name_plural = 'Звании'


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    photo = models.ImageField(upload_to='profiles/', verbose_name='Фото профиля', blank=True, null=True)
    phone_number = models.CharField(max_length=30, null=True, blank=True)
    address = models.CharField(max_length=300, null=True, blank=True)
    about = models.TextField(blank=True)
    status = models.ForeignKey(Status, on_delete=models.CASCADE, verbose_name='Статус', blank=True, null=True)
    rank = models.ForeignKey(Rank, on_delete=models.CASCADE, verbose_name='Звание', blank=True, null=True)
    instagram = models.CharField(max_length=300, blank=True, null=True)
    telegram = models.CharField(max_length=300, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания', blank=True, null=True)

    def get_photo(self):
        try:
            return self.photo.url

        except:
            return 'https://www.murrayglass.com/wp-content/uploads/2020/10/avatar-scaled.jpeg'

    def __str__(self):
        return f'{self.user.username}'

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', blank=True, null=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='Статья', blank=True, null=True)
    text = models.TextField(verbose_name='Комментарий')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='Профиль', blank=True, null=True)

    def __str__(self):
        return f'{self.user.username}'

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

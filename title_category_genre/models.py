from datetime import datetime

from django.core.validators import MaxValueValidator
from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=100, verbose_name='Жанр')
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ['-id']
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Категория')
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ['-id']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название')
    year = models.IntegerField(
        validators=[
            MaxValueValidator(
                datetime.now().year,
                message='Введен некорректный год', ),
        ]
    )
    description = models.TextField(verbose_name='Описание')
    genre = models.ManyToManyField(Genre, related_name='genres',
                                   verbose_name='Жанр')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,
                                 related_name='categories',
                                 verbose_name='Категория', blank=True,
                                 null=True)

    class Meta:
        ordering = ['-year']
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name

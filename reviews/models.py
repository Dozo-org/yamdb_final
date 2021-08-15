from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from title_category_genre.models import Title
from users.models import CustomUser as User


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение',
    )
    text = models.TextField(
        blank=False,
        verbose_name='Текст отзыва',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор отзыва',
    )
    score = models.IntegerField(
        default=5,
        validators=[
            MinValueValidator(
                1, message='Оценка должна быть больше или равна 1'
            ),
            MaxValueValidator(
                10, message='Оценка должна быть меньше 11'
            ),
        ],
        verbose_name='Оценка от автора отзыва',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата отзыва',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='Unique title-author pair',
            ),
        ]
        ordering = ['-pub_date', ]
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return self.title.name + ': ' + self.text[:7] + '...' + self.text[-3:]


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв',
    )
    text = models.TextField(
        blank=False,
        verbose_name='Текст комментария',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор комментария',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата комментария',
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text[:7] + '...' + self.text[-3:]

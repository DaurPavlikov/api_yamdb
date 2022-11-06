from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from users.models import User
from reviews.validators import validate_year


MIN_VALUE = MinValueValidator(1)
MAX_VALUE = MaxValueValidator(10)
CUTTING_LENGTH = 20


class Genre(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta():
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.slug


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta():
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self) -> str:
        return self.slug


class Title(models.Model):
    name = models.TextField()
    year = models.IntegerField(
        'Год релиза',
        validators=[validate_year],
        help_text='Введите год релиза'
    )
    genre = models.ManyToManyField(Genre, through='GenreTitle')
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name='Категория',
        help_text='Введите категорию произведения',
        null=True,
        blank=True,
        related_name='titles'
    )
    description = models.TextField(
        null=True,
        verbose_name='Описание'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self) -> str:
        return self.name


class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    class Meta():
        verbose_name = 'Жанр произведения'

    def __str__(self) -> str:
        return f'{self.genre} {self.title}'


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Название произведения',
        related_name='reviews')
    text = models.TextField(verbose_name='Текст обзора')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='reviews')
    score = models.PositiveSmallIntegerField(
        default=0,
        validators=[MIN_VALUE, MAX_VALUE],
        verbose_name='Оценка')
    pub_date = models.DateTimeField(auto_now_add=True,
                                    verbose_name='Дата обзора')

    class Meta():
        verbose_name = 'Обзор'
        verbose_name_plural = 'Обзоры'
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'], name='unique')]

    def __str__(self):
        self.text[:CUTTING_LENGTH]


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Обзор'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )
    text = models.TextField(
        verbose_name='Текст комментария',)
    pub_date = models.DateTimeField(auto_now_add=True,
                                    verbose_name='Дата обзора')

    class Meta():
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text[:CUTTING_LENGTH]

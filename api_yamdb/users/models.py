from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator


class User(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    ROLE_CHOICES = [
        (USER, 'user'),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin'),
    ]

    username = models.CharField(
        'Имя пользователя', max_length=150, unique=True, validators=[
            MinLengthValidator(
                3,
                message='username must be longer than 2 characters'
            ),
        ])
    email = models.EmailField(
        'Адрес электронной почты', unique=True, blank=False
    )
    bio = models.TextField('Биография', max_length=255, blank=True)
    password = models.CharField(max_length=100, blank=True)
    role = models.CharField(
        'Роль',
        max_length=30,
        choices=ROLE_CHOICES,
        default=USER
    )

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser

    class Meta():
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

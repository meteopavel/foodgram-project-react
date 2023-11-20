from django.contrib.auth.models import AbstractUser
from django.db import models

from users.validators import validate_username


class User(AbstractUser):
    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=128,
        unique=True,
        validators=(validate_username,)
    )
    email = models.EmailField(
        verbose_name='Электронная почта',
        max_length=128,
        unique=True
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=128,
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=128,
    )
    is_subscribed = models.BooleanField(
        'Подписан',
        default=False,
        help_text='Поставьте галочку, чтобы подписать.'
    )
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

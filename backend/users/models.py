from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=128,
        unique=True
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
        verbose_name='Имя',
        max_length=128,
    )
    is_subscribed = models.BooleanField(
        'Подписан',
        default=False,
        help_text='Поставьте галочку, чтобы подписать.'
    )

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

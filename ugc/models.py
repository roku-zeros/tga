from django.db import models
from utils.choices import *


class Profile(models.Model):
    external_id = models.PositiveIntegerField(
        verbose_name='Внешний ID пользователя',
        unique=True,
    )
    name = models.TextField(
        verbose_name='Имя пользователя',
    )

    def __str__(self):
        return f'#{self.external_id} {self.name}'

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


class Message(models.Model):
    profile = models.ForeignKey(
        to='ugc.Profile',
        verbose_name='Профиль',
        on_delete=models.PROTECT,
    )
    text = models.TextField(
        verbose_name='Текст',
    )
    created_at = models.DateTimeField(
        verbose_name='Время получения',
        auto_now_add=True,
    )

    def __str__(self):
        return f'Сообщение {self.pk} от {self.profile}'

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'


class Product(models.Model):
    name = models.CharField(
         verbose_name='Название',
    )

    country = models.CharField(
        choices=COUNTRY_CHOICES,
        verbose_name='Страна',
    )

    year = models.CharField(
        choices=YEAR_CHOICES,
        verbose_name='Год'
    )

    month = models.CharField(
        choices=MONTH_CHOICES,
        verbose_name='месяц'
    )

    direction = models.CharField(
        choices=DIRECTION_CHOICES,
        verbose_name='Направление',
    )

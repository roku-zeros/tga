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
    order_msg_id = models.PositiveIntegerField(
        verbose_name='ID сообщения с заказом',
        null=True,
    )
    order_msg = models.TextField(
        verbose_name='Сообщение заказа',
        default="",
    )
    state = models.IntegerField(default=0)
    basket = models.PositiveIntegerField(
        verbose_name='Корзина',
        null=True,
    )

    def go_next(self):
        if self.state < 5:
            self.state += 1

    def go_back(self):
        if self.state > 0:
            self.state -= 1

    def get_order(self):
        order = self.order_msg.split('\n')
        result = []
        for o in order:
            result.append(o.split(': ')[-1])
        return result

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
        max_length=30,
    )

    country = models.CharField(
        choices=COUNTRY_CHOICES,
        verbose_name='Страна',
        max_length=30,
    )

    year = models.CharField(
        choices=YEAR_CHOICES,
        verbose_name='Год',
        max_length=30,
    )

    month = models.CharField(
        choices=MONTH_CHOICES,
        verbose_name='месяц',
        max_length=30,

    )

    direction = models.CharField(
        choices=DIRECTION_CHOICES,
        verbose_name='Направление',
        max_length=30,
    )

    price = models.IntegerField(
        verbose_name='Цена (в рублях)'
    )

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class ProductChoice(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=30,
    )

    country = models.CharField(
        choices=COUNTRY_CHOICES,
        verbose_name='Страна',
        max_length=30,
    )

    year = models.CharField(
        choices=YEAR_CHOICES,
        verbose_name='Год',
        max_length=30,
    )

    month = models.CharField(
        choices=MONTH_CHOICES,
        verbose_name='месяц',
        max_length=30,

    )

    direction = models.CharField(
        choices=DIRECTION_CHOICES,
        verbose_name='Направление',
        max_length=30,
    )

    payment_method = models.CharField(
        choices=PAYMENT_CHOICE,
        verbose_name='Способ оплаты',
        max_length=30,
    )

    user = models.OneToOneField(
        Profile,
        on_delete=models.CASCADE,
        primary_key=True
    )

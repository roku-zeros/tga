# Generated by Django 3.2.5 on 2022-11-01 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ugc', '0002_alter_profile_order_msg_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='order_msg_id',
            field=models.PositiveIntegerField(null=True, verbose_name='ID сообщения с заказом'),
        ),
    ]
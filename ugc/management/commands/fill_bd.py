from django.core.management.base import BaseCommand
from utils.choices import COUNTRY_CHOICES, DIRECTION_CHOICES
from ugc.models import Product


class Command(BaseCommand):
    # Используется как описание команды обычно
    help = 'Implemented to Django application telegram bot setup command'

    def handle(self, *args, **kwargs):
        for country in COUNTRY_CHOICES:
            for year in range(2017, 2023):
                for direction in DIRECTION_CHOICES:
                    p = Product.objects.create(name="Тестовая база",
                                           country=country[0],
                                           year=year,
                                           month="",
                                           direction=direction[0],
                                           price=1
                                           )
                    with open('50.xlsx', 'rb') as excel:
                        p.file.save('50.xlsx', excel)


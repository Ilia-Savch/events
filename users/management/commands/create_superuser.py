import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from dotenv import load_dotenv

User = get_user_model()


class Command(BaseCommand):
    help = 'Создание суперпользователя, если он не существует'

    def handle(self, *args, **kwargs):
        # Загрузка переменных окружения из .env файла
        load_dotenv()

        DJANGO_SUPERUSER_USERNAME = os.getenv('DJANGO_SUPERUSER_USERNAME')
        DJANGO_SUPERUSER_EMAIL = os.getenv('DJANGO_SUPERUSER_EMAIL')
        DJANGO_SUPERUSER_PASSWORD = os.getenv('DJANGO_SUPERUSER_PASSWORD')

        # Проверка существования суперпользователя и создание нового, если его нет
        if not User.objects.filter(is_superuser=True).exists():
            User.objects.create_superuser(
                username=DJANGO_SUPERUSER_USERNAME,
                email=DJANGO_SUPERUSER_EMAIL,
                password=DJANGO_SUPERUSER_PASSWORD
            )
            self.stdout.write(self.style.SUCCESS('Суперпользователь создан.'))
        else:
            self.stdout.write(self.style.WARNING(
                'Суперпользователь уже существует.'))

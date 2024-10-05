import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
# Установка переменной окружения для настроек проекта
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

# Создание экземпляра объекта Celery
app = Celery("config")


# Загрузка настроек из файла Django
# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django apps.
# Автоматическое обнаружение и регистрация задач из файлов tasks.py в приложениях Django
app.autodiscover_tasks()


# Test task to insure workability
@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print("Все работает")

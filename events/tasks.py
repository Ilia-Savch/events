from celery import shared_task

from common.filters import get_daily_events, get_weekly_events
from common.tasks import send_reminder_email
from events.models.events import Event
from django.contrib.auth import get_user_model
User = get_user_model()


@shared_task
def send_reminder_email_on_week():
    events = get_weekly_events(Event.objects).filter(is_private=True)
    subjects = 'Напоминание о предстоящем событии'
    message_template = 'Не пропустите событие "{event_name}" уже на это неделе!'
    send_reminder_email(events, subjects, message_template)


@shared_task
def send_reminder_email_on_day():
    events = get_daily_events(query=Event.objects).filter(is_private=True)
    subjects = 'Напоминание о предстоящем событии'
    message_template = 'Не пропустите событие "{event_name}" уже сегодня!'
    send_reminder_email(events, subjects, message_template)

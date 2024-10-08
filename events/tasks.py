from celery import shared_task
import os
from django.core.mail import send_mail
from django.db.models import Q

from datetime import date, timedelta

from events.models.events import Event
from events.models.events import ParticipantInPrivateEvent
from django.contrib.auth import get_user_model
User = get_user_model()


# напоминание о предстоящем событии, на которое пользователь записан
@shared_task
def send_reminder_email_on_week(event_id: int):
    today = date.today()
    day_of_week = today.isoweekday()

    monday = today - timedelta(days=day_of_week - 1)
    sunday = monday + timedelta(days=6)

    event_on_week = Event.objects.filter(id=event_id).filter(
        Q(date_start__date__gte=monday) & Q(date_end__date__lte=sunday),).first()

    if event_on_week:
        # Ищем участника, связанного с этим событием
        participant = ParticipantInPrivateEvent.objects.filter(
            event=event_on_week.id).first()
        if participant:
            visitor = User.objects.filter(
                id=participant.participant.id).first()
            if visitor:
                send_mail(
                    subject=(
                        f'Событие "{event_on_week.name}" '
                        f'начнется уже на этой неделе.'),
                    message='Не пропустите событие!',
                    from_email=os.getenv("EMAIL_HOST_USER"),
                    recipient_list=[visitor.email],
                    fail_silently=False
                )
                print(f'"{event_on_week.name}" сообщение отправлено')
            else:
                print("Visitor not found.")
        else:
            print("Participant not found.")
    else:
        print("Event not found.")

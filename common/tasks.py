import os
from django.core.mail import send_mail

from events.models.events import ParticipantInPrivateEvent
from django.contrib.auth import get_user_model
User = get_user_model()


def send_reminder_email(events, subject, message_template):
    if events:
        for event in events:
            participants = ParticipantInPrivateEvent.objects.filter(
                event=event)
            if participants:
                for participant in participants:
                    visitor = User.objects.filter(
                        id=participant.participant.id).first()
                    if visitor:
                        message = message_template.format(
                            event_name=event.name)
                        send_mail(
                            subject=subject,
                            message=message,
                            from_email=os.getenv("EMAIL_HOST_USER"),
                            recipient_list=[visitor.email],
                            fail_silently=False
                        )
                        print(f'"{event.name}" сообщение отправлено')
                    else:
                        print("Visitor not found.")
            else:
                print("Participant not found.")
    else:
        print("Event not found.")

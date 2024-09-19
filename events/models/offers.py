from django.db import models
from django.contrib.auth import get_user_model
from events.models.events import Event
from common.models.mixins import DateMixin

User = get_user_model()


class Offer(DateMixin):
    desired_event = models.ForeignKey(
        Event, models.CASCADE, "request_event", verbose_name='Событие')
    visitor = models.ForeignKey(
        User, models.CASCADE, "offers", verbose_name="Желающий посетить"
    )
    message = models.CharField(
        'Сообщение', max_length=500, null=True, blank=True)
    event_accept = models.BooleanField('Принять', null=True, blank=True)

    class Meta:
        verbose_name = "Запрос"
        verbose_name_plural = "Запросы"

    def __str__(self):
        return f"желающий посетить {self.visitor.username} - {self.desired_event.name}"

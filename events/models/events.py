from django.db import models
from django.contrib.auth import get_user_model
from common.models.mixins import DateMixin

User = get_user_model()

#! убрать null=True, blank=True


class Event(DateMixin):
    adress = models.CharField('Адрес', max_length=500, null=True, blank=True)
    name = models.CharField('Название', max_length=500,)
    description = models.TextField('Описание', null=True, blank=True)
    is_private = models.BooleanField("Приватное событие", default=False)
    longitude = models.FloatField('Долгота', null=True, blank=True)
    latitude = models.FloatField('Широта', null=True, blank=True)
    price = models.PositiveIntegerField('Цена', default=0)
    date_start = models.DateTimeField('Дата начала')
    date_end = models.DateTimeField('Дата конца')
    organizer = models.ForeignKey(
        User, models.CASCADE, "events", verbose_name='Организатор',
    )

    class Meta:
        verbose_name = "Событие"
        verbose_name_plural = "События"

    def __str__(self):
        return f"{self.name}"


class ParticipantInPrivateEvent(models.Model):
    event = models.ForeignKey(
        'Event', models.CASCADE, "participants_event", verbose_name='Событие')
    participant = models.ForeignKey(
        User, models.CASCADE, "participants", verbose_name='Участник')

    class Meta:
        verbose_name = "Участник события"
        verbose_name_plural = "Участники событий"

    def __str__(self):
        return f"{self.event.name}({self.participant.username})"


class EventPhoto(models.Model):
    event_photo = models.ForeignKey(
        'Event', models.CASCADE, "photos", verbose_name='Событие')
    photo = models.ImageField("Фото", upload_to="ava/%Y/%m/%d")

    class Meta:
        verbose_name = "Фотография события"
        verbose_name_plural = "Фотографии событий"

    def __str__(self):
        return f"{self.event_photo.name}({self.photo})"

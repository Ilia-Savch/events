from rest_framework import serializers

from events.models.events import Event
from events.serializers.events_photos import EventPhotoSerializer


class EventListSerializer(serializers.ModelSerializer):
    photos = EventPhotoSerializer(many=True)

    class Meta:
        model = Event
        fields = (
            "id",
            "name",
            "longitude",
            "latitude",
            "adress",
            "date_start",
            "date_end",
            "photos",
        )

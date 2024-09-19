from rest_framework import serializers

from common.serializers.mixins import ExtendedModelSerializer
from events.models.events import EventPhoto, Event


class EventPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventPhoto
        fields = ("id", "photo", )


class EventPhotoCreateSerializer(ExtendedModelSerializer):
    event_photo = serializers.HiddenField(default=None)

    class Meta:
        model = EventPhoto
        fields = ("id", "photo", "event_photo",)

    def create(self, validated_data):
        event_photo = self.get_object_from_url(Event)
        validated_data["event_photo"] = event_photo
        return EventPhoto.objects.create(**validated_data)

import requests
from rest_framework import serializers

from events.models.events import Event
from events.serializers.events_photos import EventPhotoSerializer
from rest_framework.exceptions import ParseError
from common.serializers.mixins import ValidateDateSerializer

from geopy import Yandex

from users.serializers.users import UserSearchListSerializer


class EventSearchListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = (
            "id",
            "name",
            "date_start",
            "date_end",
        )


class EventRetrieveSerializer(serializers.ModelSerializer):
    photos = EventPhotoSerializer(many=True)
    organizer = UserSearchListSerializer()

    class Meta:
        model = Event
        fields = (
            "id",
            "name",
            "description",
            "is_private",
            "price",
            "longitude",
            "latitude",
            "adress",
            "date_start",
            "date_end",
            "photos",
            "organizer",
        )


class EventCreateSerializer(ValidateDateSerializer):
    organizer = serializers.HiddenField(
        default=serializers.CurrentUserDefault())
    longitude = serializers.HiddenField(default=None)
    latitude = serializers.HiddenField(default=None)

    class Meta:
        model = Event
        fields = (
            "id",
            "name",
            "adress",
            "description",
            "is_private",
            "longitude",
            "latitude",
            "date_start",
            "date_end",
            "price",
            "organizer",
        )

    def validate(self, attrs):
        return super().validate_date(attrs)

    #! убрать условие
    #! убрать api_key в env
    def create(self, validated_data):
        adress = validated_data["adress"]
        if adress == "":
            return Event.objects.create(**validated_data)
        location = Yandex(
            api_key="54e34056-8d9c-435d-84b8-d68729ef0897").geocode(adress)
        if location == None:
            raise ParseError("Адрес не найден")
        longitude = location.longitude
        latitude = location.latitude
        validated_data["longitude"] = longitude
        validated_data["latitude"] = latitude
        return Event.objects.create(**validated_data)


class EventUpdateSerializer(ValidateDateSerializer):
    longitude = serializers.HiddenField(default=None)
    latitude = serializers.HiddenField(default=None)

    class Meta:
        model = Event
        fields = (
            "id",
            "name",
            "adress",
            "description",
            "date_start",
            "date_end",
            "price",
            "longitude",
            "latitude",
        )

    def validate(self, attrs):
        return super().validate_date(attrs)

    def update(self, instance, validated_data):
        old_adress = instance.adress
        adress = validated_data.get("adress", None)

        if old_adress != adress:
            try:
                location = Yandex(
                    api_key="54e34056-8d9c-435d-84b8-d68729ef0897").geocode(adress)
                if location == None:
                    raise ParseError("Адрес не найден")

                longitude = location.longitude
                latitude = location.latitude

                instance.adress = adress
                instance.longitude = longitude
                instance.latitude = latitude
            except requests.RequestException as e:
                raise ParseError(f"Ошибка при запросе к геокодеру: {str(e)}")

        # Обновление всех остальных полей экземпляра модели
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        return super().update(instance, validated_data)

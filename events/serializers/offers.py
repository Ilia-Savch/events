from common.serializers.mixins import ExtendedModelSerializer
from events.models.offers import Offer
from events.models.events import Event, ParticipantInPrivateEvent
from events.serializers.events import EventSearchListSerializer
from users.serializers.users import UserSearchListSerializer

from rest_framework import serializers
from rest_framework.exceptions import ParseError

from django.db import transaction

from django.utils import timezone


class OfferListSerializer(serializers.ModelSerializer):
    desired_event = EventSearchListSerializer()
    visitor = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Offer
        fields = (
            "id",
            "desired_event",
            "event_accept",
            "visitor",
            "created_at",
            "updated_at",
        )


class OfferRetrieveSerializer(serializers.ModelSerializer):
    desired_event = EventSearchListSerializer()

    class Meta:
        model = Offer
        fields = (
            "id",
            "desired_event",
            "message",
            "event_accept",
        )

#######################################
# SERIALIZERS REQUEST FOR USER
#######################################


class OfferCreateSerializer(ExtendedModelSerializer):
    visitor = serializers.HiddenField(default=serializers.CurrentUserDefault())
    desired_event = serializers.HiddenField(default=None)
    event_accept = serializers.HiddenField(default=None)

    class Meta:
        model = Offer
        fields = (
            "id",
            "visitor",
            "desired_event",
            "message",
            "event_accept",
        )

    def validate(self, attrs):
        desired_event = self.get_object_from_url(Event)
        visitor = attrs['visitor']

        request_exist = self.Meta.model.objects.filter(
            visitor=visitor,
            desired_event=desired_event,
        ).exists()
        if request_exist:
            raise ParseError("Вы уже подали заявку на это событие")

        already_accept = desired_event.participants_event.filter(
            participant=visitor).exists()
        if already_accept:
            raise ParseError("Вы уже являетесь участником данного события")

        if desired_event.organizer == visitor:
            raise ParseError("Вы не можете подать заявку на свое событие")

        if desired_event.date_end <= timezone.now():
            raise ParseError("Событие уже прошло")

        return attrs

    def create(self, validated_data):
        desired_event = self.get_object_from_url(Event)
        validated_data["desired_event"] = desired_event

        if desired_event.is_private == True:
            return Offer.objects.create(**validated_data)
        else:
            return ParseError("Событие не закрытое")


class OfferUpdateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Offer
        fields = (
            "id",
            "message",
        )


#######################################
# SERIALIZERS REQUEST FOR EVENT OWENER
#######################################


class OfferUpdateEventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Offer
        fields = (
            "id",
            "event_accept",
        )

    def validate(self, attrs):
        attrs['event_accept'] = attrs.pop('event_accept')

        if self.instance.event_accept is not None:
            raise ParseError("Заявка закрыта. Изменение недоступно.")
        return attrs

    def update(self, instance, validated_data):
        with transaction.atomic():
            instance = super().update(instance, validated_data)
            if instance.event_accept:
                participant = ParticipantInPrivateEvent(
                    event=instance.desired_event, participant=instance.visitor)
                participant.save()
                instance.desired_event.participants_event.add(participant)
        return instance

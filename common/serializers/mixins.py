from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from rest_framework.exceptions import ParseError
from datetime import date

from events.models.events import Event


class ExtendedModelSerializer(serializers.ModelSerializer):
    class Meta:
        abstract = True

    def get_from_url(self, lookup_field):
        assert "view" in self.context, (
            'No view context in "%s". '
            "Check parameter context on function calling." % self.__class__.__name__
        )
        assert self.context["view"].kwargs.get(lookup_field), (
            'Got no data from url in  "%s". ' "Check lookup field on function calling."
        )
        value = self.context["view"].kwargs.get(lookup_field)
        return value

    def get_object_from_url(self, model, lookup_field="pk", model_field="pk"):
        obj_id = self.get_from_url(lookup_field)
        obj = get_object_or_404(
            queryset=model.objects.all(), **{model_field: obj_id})
        return obj


class ValidateDateSerializer(ExtendedModelSerializer):
    class Meta:
        abstract = True

    def validate_date(self, attrs):
        if "date_start" not in attrs or "date_end" not in attrs:
            return attrs

        today = date.today()
        date_start = attrs["date_start"]
        date_end = attrs["date_end"]

        if date_start.date() <= today:
            raise ParseError(
                "Время начала события не может быть раньше текущего")
        if date_start == date_end:
            raise ParseError(
                "Время начала и конца события не должны совпадать")
        if date_start > date_end:
            raise ParseError(
                "Время начала события не может быть позже времени его окончания")
        return attrs

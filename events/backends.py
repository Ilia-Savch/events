from django.db.models import Q
from rest_framework.filters import BaseFilterBackend


class MyEventsFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        user = request.user
        return queryset.filter(Q(organizer=user))


class OfferEventFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        user = request.user
        return queryset.filter(Q(desired_event__organizer=user))


class OfferUserFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        user = request.user
        return queryset.filter(Q(visitor=user))

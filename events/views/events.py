from rest_framework import mixins
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from common.views.mixins import ExtendedGenericViewSet, CRUDViewSet, ListViewSet, clear_cache, get_cached_queryset, log_db_queries
from events.backends import MyEventsFilter
from events.filters import DateTimeFilter
from events.permissions import IsOrganiserOrReadOnly, IsOwner, IsParticipantInPrivateEvent
from events.serializers import events as events_s
from events.serializers import events_photos as events_photos_s
from events.serializers import common as common_s
from datetime import date
import time

from events.models.events import Event, EventPhoto
from django.contrib.auth import get_user_model

User = get_user_model()

# EventView


@receiver(post_save, sender=Event)
def clear_event_cache_on_save(sender, instance, **kwargs):
    clear_cache(instance, prefix="events_queryset")


@receiver(post_delete, sender=Event)
def clear_event_cache_on_delete(sender, instance, **kwargs):
    clear_cache(instance, prefix="events_queryset")

# MyEventView


@receiver(post_save, sender=User)
def clear_event_cache_on_save(sender, instance, **kwargs):
    clear_cache(instance, prefix="my_events_list_queryset")


@receiver(post_delete, sender=User)
def clear_event_cache_on_delete(sender, instance, **kwargs):
    clear_cache(instance, prefix="my_events_list_queryset")


@extend_schema_view(
    retrieve=extend_schema(summary="Деталка событий", tags=["События"]),
    create=extend_schema(summary="Создать событие", tags=["События"]),
    partial_update=extend_schema(
        summary="Изменить событие частично", tags=["События"]),
    destroy=extend_schema(summary=("Удалить событие"), tags=["События"]),
)
class EventView(CRUDViewSet):
    permission_classes = [
        IsAuthenticated,
        IsOrganiserOrReadOnly,
        IsOwner,
        IsParticipantInPrivateEvent,
    ]
    queryset = Event.objects.all()
    serializer_class = common_s.EventListSerializer
    multi_serializer_class = {
        "retrieve": events_s.EventRetrieveSerializer,
        "create": events_s.EventCreateSerializer,
        "partial_update": events_s.EventUpdateSerializer,
    }
    http_method_names = ("get", "post", "patch", "delete")

    @log_db_queries
    def get_queryset(self):
        event_id = self.kwargs.get('pk')
        cache_key = f"events_queryset_{event_id}"

        return get_cached_queryset(Event, cache_key, ["organizer",], ["photos", "participants_event",])


@extend_schema_view(
    list=extend_schema(summary="Список событий", tags=["События"]),
    search=extend_schema(
        filters=True, summary="Список событий Search", tags=["Словари"]
    ),
)
class EventListView(ListViewSet):
    queryset = Event.objects.all()
    serializer_class = common_s.EventListSerializer
    multi_serializer_class = {
        "list": common_s.EventListSerializer,
        "search": events_s.EventSearchListSerializer,
    }
    http_method_names = ("get",)

    @action(methods=["GET"], detail=False, url_path="search")
    def search(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    filter_backends = (
        OrderingFilter,
        SearchFilter,
        DjangoFilterBackend,
    )
    filterset_class = DateTimeFilter

    search_fields = (
        "name",
        "organizer",
        "adress",
    )
    ordering = (
        "name",
        "id",
        "organizer",
        "is_private",
        "date_start",
    )

    @log_db_queries
    def get_queryset(self):
        cache_key = f"events_list_queryset"

        return get_cached_queryset(Event, cache_key, ["organizer",], ["photos",], timeout=5*60)


@extend_schema_view(
    list=extend_schema(summary="Список моих событий", tags=["События"]),
    search=extend_schema(
        filters=True, summary="Список моих событий Search", tags=["Словари"]
    ),
)
class MyEventView(ListViewSet):
    queryset = Event.objects.all()
    serializer_class = common_s.EventListSerializer
    multi_serializer_class = {
        "list": common_s.EventListSerializer,
        "search": events_s.EventSearchListSerializer,
    }
    http_method_names = ("get",)

    @action(methods=["GET"], detail=False, url_path="search")
    def search(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    filter_backends = (
        OrderingFilter,
        SearchFilter,
        DjangoFilterBackend,
        MyEventsFilter,
    )
    filterset_class = DateTimeFilter

    search_fields = (
        "name",
        "organizer",
        "adress",
    )
    ordering = (
        "name",
        "id",
        "organizer",
    )

    @log_db_queries
    def get_queryset(self):
        user_id = self.request.user.id
        cache_key = f"my_events_list_queryset_{user_id}"

        return get_cached_queryset(Event, cache_key, ["organizer",], ["photos",])


@extend_schema_view(
    create=extend_schema(
        summary="Добавить фото события",
        tags=["События: Фотографии"]
    ),
    destroy=extend_schema(
        summary="Удалить фото события",
        tags=["События: Фотографии"]
    )
)
class EventPhotoView(ExtendedGenericViewSet, mixins.CreateModelMixin, mixins.DestroyModelMixin):
    permission_classes = [
        IsAuthenticated,
        IsOrganiserOrReadOnly,
        IsOwner,
    ]
    queryset = EventPhoto.objects.all()
    serializer_class = events_photos_s.EventPhotoCreateSerializer
    http_method_names = ("post", "delete",)
    lookup_url_kwarg = "event_photo_id"

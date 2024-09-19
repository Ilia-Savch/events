from rest_framework import mixins
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from common.views.mixins import ExtendedGenericViewSet, CRUDViewSet, ListViewSet
from events.backends import MyEventsFilter
from events.filters import DateTimeFilter
from events.permissions import IsOrganiserOrReadOnly, IsOwner, IsParticipantInPrivateEvent
from events.serializers import events as events_s
from events.serializers import events_photos as events_photos_s
from events.serializers import common as common_s
from datetime import date

from events.models.events import Event, EventPhoto


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

    def get_queryset(self):
        queryset = Event.objects.select_related(
            "organizer",
        )
        return queryset


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

    def get_queryset(self):
        queryset = Event.objects.select_related(
            "organizer",
        ).filter(date_end__gte=date.today())
        return queryset


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

    def get_queryset(self):
        queryset = Event.objects.select_related(
            "organizer",
        )
        return queryset


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

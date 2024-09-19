from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated


from common.views.mixins import CreateViewSet, LURDViewSet, ListViewSet
from events.backends import OfferEventFilter, OfferUserFilter
from events.models.offers import Offer
from events.permissions import IsOwnerOfferEvent, IsOwnerOfferUser
from events.serializers import offers as offers_s


@extend_schema_view(
    list=extend_schema(
        summary='Список запросов для организатора',
        tags=['События: Запросы']),
    retrieve=extend_schema(
        summary='Деталка запроса для организатора',
        tags=['События: Запросы']),
    partial_update=extend_schema(
        summary='Изменить запрос для организатора частично', tags=['События: Запросы']),
    destroy=extend_schema(
        summary='Удалить запрос для организатора', tags=['События: Запросы']),
)
class OfferEventView(LURDViewSet):
    permission_classes = [
        IsAuthenticated,
        IsOwnerOfferEvent,
    ]

    queryset = Offer.objects.all()
    serializer_class = offers_s.OfferListSerializer

    multi_serializer_class = {
        'list': offers_s.OfferListSerializer,
        'retrieve': offers_s.OfferRetrieveSerializer,
        'partial_update': offers_s.OfferUpdateEventSerializer,
    }

    http_method_names = ('get', 'patch', 'delete',)

    filter_backends = (
        DjangoFilterBackend,
        OrderingFilter,
        SearchFilter,
        OfferEventFilter,
    )

    ordering_fields = ('-created_at', 'updated_at', 'desired_event')

    search_fields = ('desired_event__name',)

    def get_queryset(self):
        return Offer.objects.select_related('desired_event', 'visitor')


@extend_schema_view(
    list=extend_schema(
        summary='Список запросов для пользователя',
        tags=['События: Запросы']),
    retrieve=extend_schema(
        summary='Деталка запроса для пользователя',
        tags=['События: Запросы']),
    partial_update=extend_schema(
        summary='Изменить запрос для пользователя частично', tags=['События: Запросы']),
    destroy=extend_schema(
        summary='Удалить запрос для пользователя', tags=['События: Запросы']),
)
class OfferUserView(LURDViewSet):
    permission_classes = [
        IsAuthenticated,
        IsOwnerOfferUser,
    ]
    queryset = Offer.objects.all()
    serializer_class = offers_s.OfferListSerializer
    multi_serializer_class = {
        'list': offers_s.OfferListSerializer,
        'retrieve': offers_s.OfferRetrieveSerializer,
        'partial_update': offers_s.OfferUpdateUserSerializer,
    }
    http_method_names = ("get", 'patch', 'post', 'delete')

    filter_backends = (
        DjangoFilterBackend,
        OrderingFilter,
        SearchFilter,
        OfferUserFilter,
    )

    search_fields = (
        "desired_event__name",
    )

    ordering_fields = ('-created_at', 'updated_at', 'desired_event')

    def get_queryset(self):
        return Offer.objects.select_related('desired_event', 'visitor')


@extend_schema_view(
    create=extend_schema(
        summary='Создать запрос для пользователя', tags=['События: Запросы']),
)
class OfferUserCreateView(CreateViewSet):
    permission_classes = [
        IsAuthenticated,
        IsOwnerOfferUser,
    ]

    queryset = Offer.objects.all()
    serializer_class = offers_s.OfferCreateSerializer

    lookup_url_kwarg = 'offer_id'

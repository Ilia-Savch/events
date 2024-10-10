from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated


from common.views.mixins import CreateViewSet, LUDViewSet, ListViewSet, clear_cache, get_cached_queryset, log_db_queries
from events.backends import OfferEventFilter, OfferUserFilter
from events.models.offers import Offer
from django.contrib.auth import get_user_model
from events.permissions import IsOwnerOfferEvent, IsOwnerOfferUser
from events.serializers import offers as offers_s

from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

import time

User = get_user_model()

# OfferEventView


@receiver(post_save, sender=User)
def clear_event_cache_on_save(sender, instance, **kwargs):
    clear_cache(instance, prefix="offers_event_queryset")


@receiver(post_delete, sender=User)
def clear_event_cache_on_delete(sender, instance, **kwargs):
    clear_cache(instance, prefix="offers_event_queryset")

# OfferUserView


@receiver(post_save, sender=User)
def clear_event_cache_on_save(sender, instance, **kwargs):
    clear_cache(instance, prefix="offers_user_queryset")


@receiver(post_delete, sender=User)
def clear_event_cache_on_delete(sender, instance, **kwargs):
    clear_cache(instance, prefix="offers_user_queryset")


@extend_schema_view(
    list=extend_schema(
        summary='Список запросов для организатора',
        tags=['События: Запросы']),
    partial_update=extend_schema(
        summary='Изменить запрос для организатора частично', tags=['События: Запросы']),
    destroy=extend_schema(
        summary='Удалить запрос для организатора', tags=['События: Запросы']),
)
class OfferEventView(LUDViewSet):
    permission_classes = [
        IsAuthenticated,
        IsOwnerOfferEvent,
    ]

    queryset = Offer.objects.all()
    serializer_class = offers_s.OfferListEventsSerializer

    multi_serializer_class = {
        'list': offers_s.OfferListEventsSerializer,
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

    @log_db_queries
    def get_queryset(self):
        user_id = self.request.user.pk
        cache_key = f"offers_event_queryset_{user_id}"

        return get_cached_queryset(
            Offer, cache_key, ['desired_event', 'visitor'],
        )


@extend_schema_view(
    list=extend_schema(
        summary='Список запросов для пользователя',
        tags=['События: Запросы']),
    partial_update=extend_schema(
        summary='Изменить запрос для пользователя частично', tags=['События: Запросы']),
    destroy=extend_schema(
        summary='Удалить запрос для пользователя', tags=['События: Запросы']),
)
class OfferUserView(LUDViewSet):
    permission_classes = [
        IsAuthenticated,
        IsOwnerOfferUser,
    ]
    queryset = Offer.objects.all()
    serializer_class = offers_s.OfferListUserSerializer
    multi_serializer_class = {
        'list': offers_s.OfferListUserSerializer,
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

    @log_db_queries
    def get_queryset(self):
        user_id = self.request.user.pk
        cache_key = f"offers_user_queryset_{user_id}"

        return get_cached_queryset(
            Offer, cache_key, ['desired_event',],
        )


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

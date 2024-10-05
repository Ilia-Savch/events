import time
from rest_framework import mixins
from rest_framework.generics import GenericAPIView
from django.core.cache import cache

from rest_framework.viewsets import GenericViewSet


class ExtendedView:
    multi_permission_classes = None
    multi_serializer_class = None
    request = None

    def get_serializer_class(self):
        assert self.serializer_class or self.multi_serializer_class, (
            '"%s" should either include `serializer_class`, '
            "`multi_serializer_class`, attribute, or override the "
            "`get_serializer_class()` method." % self.__class__.__name__
        )
        if not self.multi_serializer_class:
            return self.serializer_class

        # define request action or method
        if hasattr(self, "action") and self.action:
            action = self.action
        else:
            action = self.request.method

        # Trying to get action serializer or default
        return self.multi_serializer_class.get(action) or self.serializer_class

    def get_permissions(self):
        # define request action or method
        if hasattr(self, "action"):
            action = self.action
        else:
            action = self.request.method

        if self.multi_permission_classes:
            permissions = self.multi_permission_classes.get(action)
            if permissions:
                return [permission() for permission in permissions]

        return [permission() for permission in self.permission_classes]


class ExtendedGenericViewSet(ExtendedView, GenericViewSet):
    pass


class ListViewSet(ExtendedGenericViewSet, mixins.ListModelMixin):
    pass


class RetrieveViewSet(ExtendedGenericViewSet, mixins.RetrieveModelMixin,):
    pass


class CreateViewSet(ExtendedGenericViewSet, mixins.CreateModelMixin,):
    pass


class LUDViewSet(ExtendedGenericViewSet, mixins.ListModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    pass


class LCRUViewSet(
    ExtendedGenericViewSet,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
):
    pass


class LCRUDViewSet(
    LCRUViewSet,
    mixins.DestroyModelMixin,
):
    pass


class CRUDViewSet(
    ExtendedGenericViewSet,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
):
    pass

###########################
# CACHE
###########################


def clear_cache(instance, prefix="prefix"):
    """
    Универсальная функция для очистки кэша.
    """
    cache_key = f"{prefix}_{instance.pk}"
    cache.delete(cache_key)


def get_cached_queryset(model, cache_key, select_related_fields=None, prefetch_related_fields=None, timeout=15*60):
    cache_queryset = cache.get(cache_key)

    if cache_queryset is None:
        if prefetch_related_fields:
            queryset = model.objects.select_related(
                *select_related_fields).prefetch_related(*prefetch_related_fields)
        else:
            queryset = model.objects.select_related(
                *select_related_fields)
        cache.set(cache_key, queryset, timeout=timeout)
        return queryset
    else:
        return cache_queryset


def log_db_queries(f):
    from django.db import connection

    def new_f(* args, ** kwargs):
        start_time = time.time()
        res = f(* args, ** kwargs)
        print("\n\n")
        print("-"*80)
        print("db queries log for %s:\n" % (f.__name__))
        print(" TOTAL COUNT : % s " % len(connection.queries))
        for q in connection.queries:
            print("%s: %s\n" % (q["time"], q["sql"]))
        end_time = time.time()
        duration = end_time - start_time
        print('\n Total time: {:.3f} ms'.format(duration * 1000.0))
        print("-"*80)
        return res
    return new_f

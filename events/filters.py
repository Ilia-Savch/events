from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from django.db.models import Q
from django_filters import FilterSet, filters

from events.models.events import Event
from events.models.offers import Offer


class DateTimeFilter(FilterSet):
    is_today = filters.BooleanFilter(method='is_today_filter')
    is_on_week = filters.BooleanFilter(method='is_on_week_filter')
    is_on_month = filters.BooleanFilter(method="is_on_month_filter")

    class Meta:
        model = Event
        fields = (
            "is_on_month", "is_on_week",
            "is_today", "date_start", "date_end"
        )

    def is_today_filter(self, queryset, name, value):
        now = datetime.now()  # текущая дата и время
        return queryset.filter(
            Q(date_start__date=date.today(), date_start__time__lte=now.time()) &
            Q(date_end__date=date.today(), date_end__time__gte=now.time())
        )

    def is_on_week_filter(self, queryset, name, value):
        today = date.today()
        day_of_week = today.isoweekday()

        monday = today - timedelta(days=day_of_week - 1)
        sunday = monday + timedelta(days=6)

        return queryset.filter(
            Q(date_start__date__gte=monday) & Q(date_end__date__lte=sunday)
        )

    def is_on_month_filter(self, queryset, name, value):
        today = date.today()
        start_of_month = today.replace(day=1)
        end_of_month = start_of_month + \
            relativedelta(months=1) - timedelta(days=1)

        return queryset.filter(Q(date_start__date__gte=start_of_month) & Q(date_end__date__lte=end_of_month))

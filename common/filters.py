from datetime import date, timedelta, datetime
from django.db.models import Q


def get_weekly_events(query):
    today = date.today()
    day_of_week = today.isoweekday()

    monday = today - timedelta(days=day_of_week - 1)
    sunday = monday + timedelta(days=6)

    events = query.filter(
        Q(date_start__date__gte=monday) & Q(date_end__date__lte=sunday)
    )
    return events


def get_daily_events(query):
    now = datetime.now()
    events = query.filter(
        Q(date_start__date=date.today(), date_start__time__lte=now.time()) &
        Q(date_end__date=date.today(), date_end__time__gte=now.time())
    )
    return events

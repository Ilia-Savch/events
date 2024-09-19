from django.contrib import admin
from events.models import events, offers
from common.admin import DateMixinAdmin

##############################
# INLINES
##############################


class ExchangeInline(admin.TabularInline):
    model = offers.Offer
    fields = (
        "event_accept",
        "desired_event",
    )

##############################
# MODELS
##############################


@admin.register(events.Event)
class EventAdmin(DateMixinAdmin):
    list_display = (
        "id",
        "name",
        "adress",
        "description",
        "is_private",
        "longitude",
        "latitude",
        "price",
        "date_start",
        "date_end",
        "organizer",
    )
    list_filter = ("is_private",)
    search_fields = ("name__startswith",)
    readonly_fields = ("created_at", "updated_at",)


@admin.register(events.EventPhoto)
class EventPhotoAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "event_photo",
        "photo_display",
    )
    search_fields = ("event_photo__name",)
    raw_id_fields = ['event_photo', ]
    list_select_related = ['event_photo', ]

    def photo_display(self, obj):
        return obj.photo.url if obj.photo else "No image"

    photo_display.short_description = "Фотографии"


@admin.register(offers.Offer)
class OfferAdmin(DateMixinAdmin):
    list_display = ("id", "desired_event", "visitor",
                    "message", "event_accept",)
    search_fields = ("desired_event__name", "visitor__username",)
    list_filter = ("event_accept",)

    raw_id_fields = ['desired_event', ]
    list_select_related = ['desired_event', ]


@admin.register(events.ParticipantInPrivateEvent)
class ParticipantInPrivateEventAdmin(admin.ModelAdmin):
    list_display = ("id", "participant", "event",)
    search_fields = ("event__name", "participant__username",)

    raw_id_fields = ['event', ]
    list_select_related = ['event', ]

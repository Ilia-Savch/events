from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.urls import path
from events.views import events, offers


router = DefaultRouter()


router.register(
    r"(?P<pk>\d+)/offers/user/create", offers.OfferUserCreateView, "offers_create"
)
router.register(r"offers/user", offers.OfferUserView, "users_offers")
router.register(r"offers/organizer", offers.OfferEventView, "events_offers")


router.register(
    r"(?P<pk>\d+)/photos", events.EventPhotoView, "events_photos"
)
router.register(r"list", events.EventListView, "events_list")
router.register(r"my", events.MyEventView, "events_my")

router.register(r"", events.EventView, "events")

urlpatterns = [
    path("events/", include(router.urls)),
]

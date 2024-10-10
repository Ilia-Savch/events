from django.urls import path, include

from api.spectacular.urls import urlpatterns as doc_urls
from events.urls import urlpatterns as event_urls
from users.urls import urlpatterns as user_urls

# from users.urls import urlpatterns as user_urls

app_name = "api"

urlpatterns = [
    path("auth/", include("djoser.urls.jwt")),
]
# urlpatterns += user_urls
urlpatterns += doc_urls
urlpatterns += event_urls
urlpatterns += user_urls

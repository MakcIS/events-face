from django.urls import path

from src.events.views import EventsList

urlpatterns = [
    path("", EventsList.as_view(), name="events_list"),
]

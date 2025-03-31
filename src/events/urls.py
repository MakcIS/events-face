from django.urls import path

from .views import EventsList

urlpatterns = [
    path("", EventsList.as_view(), name="events_list"),
]

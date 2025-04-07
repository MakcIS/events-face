from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListAPIView
from rest_framework.pagination import CursorPagination
from rest_framework.permissions import IsAuthenticated

from src.events.models import Events
from src.events.serializer import EventsSerializer


class EventsPagination(CursorPagination):
    page_size = 10


# Подумать над кешированием для снижения нагрузки на БД
class EventsList(ListAPIView):
    queryset = Events.objects.select_related("place").filter(status="open")
    serializer_class = EventsSerializer
    filter_backends = [OrderingFilter, SearchFilter]
    pagination_class = EventsPagination
    permission_classes = [IsAuthenticated]
    search_fields = ["name"]
    ordering_fields = ["date"]
    ordering = ["date"]


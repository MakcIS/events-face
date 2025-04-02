from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListAPIView
from rest_framework.pagination import CursorPagination
from rest_framework.permissions import IsAuthenticated

from .models import Events
from .serializer import EventsSerializer


class EventsPagination(CursorPagination):
    page_size = 10


# Подумать над кешированием для снижения нагрузки на БД
class EventsList(ListAPIView):
    serializer_class = EventsSerializer
    filter_backends = [OrderingFilter, SearchFilter]
    pagination_class = EventsPagination
    permission_classes = [IsAuthenticated]
    search_fields = ["name"]
    ordering_fields = ["date"]
    ordering = ["date"]

    def get_queryset(self):
        data = Events.objects.select_related("place").filter(status="open")
        return data

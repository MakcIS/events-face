from django.contrib import admin

from src.events.models import Events, Places


@admin.register(Places)
class PlacesAdmin(admin.ModelAdmin):
    list_display = ["name"]
    list_display_links = ["name"]


@admin.register(Events)
class EventsAdmin(admin.ModelAdmin):
    list_display = ["name", "date", "status", "place"]
    list_display_links = ["name"]
    list_select_related = ["place"]

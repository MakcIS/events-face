from django.contrib import admin

from src.sync.models import EventsSync


@admin.register(EventsSync)
class EventSyncAdmin(admin.ModelAdmin):
    list_display = ["sync_date", "created", "updated", "changed_at"]

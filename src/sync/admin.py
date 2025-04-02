from django.contrib import admin

from .models import EventsSync


@admin.register(EventsSync)
class EventSyncAdmin(admin.ModelAdmin):
    list_display = ["sync_date", "created", "updated", "changed_at"]

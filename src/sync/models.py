from django.db import models


class EventsSync(models.Model):
    sync_date = models.DateTimeField(
        verbose_name="Дата и время синхронизации", auto_now_add=True,
    )
    created = models.IntegerField(
        verbose_name="Созданно", help_text="Сколько событий было созданно", default=0,
    )
    updated = models.IntegerField(
        verbose_name="Обновлено", help_text="Сколько событий было созданно", default=0,
    )
    changed_at = models.DateField(
        verbose_name="Дата изменения", help_text="Дата изменения событий",
        null=True, default=None,
    )

    class Meta:
        verbose_name = "Синхронизация Событий"

    def __str__(self):
        return f"{self.sync_date}"

import uuid

from django.db import models


class EventStatus(models.TextChoices):
    OPEN = "open"
    CLOSED = "closed"


class Places(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4())
    name = models.CharField(max_length=255, verbose_name="Название площадки")

    class Meta:
        verbose_name = "Место"
        verbose_name_plural = "Места"

    def __str__(self):
        return f"{self.name}"


class Events(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4())
    name = models.CharField(max_length=255, verbose_name="Название мероприятия")
    date = models.DateField(verbose_name="Дата проведения")
    status = models.CharField(
        verbose_name="Статус мероприятия", choices=EventStatus.choices, max_length=10
    )
    place = models.ForeignKey(
        Places,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Место проведения",
    )

    class Meta:
        verbose_name = "Мероприятие"
        verbose_name_plural = "Мероприятия"

    def __str__(self):
        return f"{self.name}"

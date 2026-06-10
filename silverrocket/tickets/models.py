import uuid

from core.mixins import DisplayIDMixin
from django.conf import settings
from django.db import models


class Ticket(DisplayIDMixin, models.Model):
    display_prefix = "TKT"

    class Status(models.IntegerChoices):
        OPEN = 1, "Open"
        IN_PROGRESS = 2, "In Progress"
        CLOSED = 3, "Closed"

    class Priority(models.IntegerChoices):
        LOW = 1, "Low"
        MEDIUM = 2, "Medium"
        HIGH = 3, "High"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    title = models.CharField(max_length=255)
    description = models.TextField()

    status = models.SmallIntegerField(
        choices=Status.choices,
        default=Status.OPEN,
    )

    priority = models.SmallIntegerField(
        choices=Priority.choices,
        default=Priority.MEDIUM,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="tickets_created",
        null=False,
    )

    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="tickets_assigned",
        null=True,
        blank=True,
    )

    # TODO: Add device relationship after the devices app and Device model are created.
    # devices = models.ManyToManyField(
    #     "devices.Device",
    #     blank=True,
    #     related_name="tickets",
    # )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"

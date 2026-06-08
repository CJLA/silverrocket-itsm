from django.contrib import admin

from .models import Ticket


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = (
        "display_id",
        "title",
        "status",
        "priority",
        "created_by",
        "assigned_to",
        "created_at",
        "updated_at",
    )

    list_filter = (
        "status",
        "priority",
        "created_at",
    )

    search_fields = (
        "title",
        "description",
        "created_by__email",
        "assigned_to__email",
    )

    list_select_related = (
        "created_by",
        "assigned_to",
    )

    readonly_fields = (
        "display_id",
        "created_at",
        "updated_at",
    )

    ordering = ("-created_at",)

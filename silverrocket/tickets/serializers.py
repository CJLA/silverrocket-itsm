from rest_framework import serializers

from .models import Ticket


class TicketCardSerializer(serializers.ModelSerializer):
    """
    Compact serializer for Kanban cards.
    """

    status_display = serializers.CharField(source="get_status_display", read_only=True)
    priority_display = serializers.CharField(
        source="get_priority_display", read_only=True
    )

    class Meta:
        model = Ticket
        fields = [
            "id",
            "display_id",
            "title",
            "status",
            "status_display",
            "priority",
            "priority_display",
            "assigned_to",
            "created_at",
            "updated_at",
        ]


class TicketDetailSerializer(serializers.ModelSerializer):
    """
    Detailed serializer for ticket views.
    """

    status_display = serializers.CharField(source="get_status_display", read_only=True)
    priority_display = serializers.CharField(
        source="get_priority_display", read_only=True
    )
    created_by_name = serializers.SerializerMethodField(read_only=True)
    assigned_to_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Ticket
        fields = [
            "id",
            "display_id",
            "title",
            "description",
            "status",
            "status_display",
            "priority",
            "priority_display",
            "created_by",
            "created_by_name",
            "assigned_to",
            "assigned_to_name",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "display_id",
            "created_by",
            "created_at",
            "updated_at",
        ]

    def get_created_by_name(self, obj):
        return obj.created_by.get_full_name() or obj.created_by.email

    def get_assigned_to_name(self, obj):
        if obj.assigned_to:
            return obj.assigned_to.get_full_name() or obj.assigned_to.email
        return None


class TicketDropDownSerializer(serializers.ModelSerializer):
    """
    Minimal serializer for dropdown selections.
    """

    title_id_label = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Ticket
        fields = ["id", "display_id", "title", "title_id_label"]

    def get_title_id_label(self, obj):
        return f"{obj.display_id} - {obj.title}"

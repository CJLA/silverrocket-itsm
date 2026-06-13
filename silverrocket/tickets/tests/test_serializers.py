from accounts.models import CustomUser
from django.test import TestCase

from tickets.models import Ticket
from tickets.serializers import (
    TicketCardSerializer,
    TicketDetailSerializer,
    TicketDropDownSerializer,
)


class TicketDetailSerializerTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = CustomUser.objects.create_user(
            email="test@example.com",
            password="testpass123",
        )

        cls.ticket = Ticket.objects.create(
            title="Test Ticket",
            description="This is a test ticket.",
            created_by=cls.user,
        )

    def test_created_by_name_falls_back_to_email_when_name_is_blank(self):
        serializer = TicketDetailSerializer(self.ticket)

        self.assertEqual(
            serializer.data["created_by_name"],
            "test@example.com",
        )

    def test_created_by_name_uses_full_name_when_available(self):
        user = CustomUser.objects.create_user(
            email="test2@example.com",
            password="testpass123",
            first_name="Solomon",
            last_name="Grundy",
        )

        ticket = Ticket.objects.create(
            title="Named User Ticket",
            description="This ticket has a named creator.",
            created_by=user,
        )

        serializer = TicketDetailSerializer(ticket)

        self.assertEqual(
            serializer.data["created_by_name"],
            "Solomon Grundy",
        )

    def test_assigned_to_name_is_none_when_ticket_is_unassigned(self):
        serializer = TicketDetailSerializer(self.ticket)

        self.assertIsNone(serializer.data["assigned_to_name"])

    def test_status_and_priority_display_values_are_serialized(self):
        serializer = TicketDetailSerializer(self.ticket)

        self.assertEqual(serializer.data["status_display"], "Open")
        self.assertEqual(serializer.data["priority_display"], "Medium")


class TicketDropdownSerializerTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = CustomUser.objects.create_user(
            email="test@example.com",
            password="testpass123",
        )

        cls.ticket = Ticket.objects.create(
            title="Test Ticket",
            description="This is a test ticket.",
            created_by=cls.user,
        )

    def test_label_includes_display_id_and_title(self):
        serializer = TicketDropDownSerializer(self.ticket)

        self.assertEqual(
            serializer.data["title_id_label"],
            f"{self.ticket.display_id} - Test Ticket",
        )


class TicketCardSerializerTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = CustomUser.objects.create_user(
            email="test@example.com",
            password="testpass123",
        )

        cls.ticket = Ticket.objects.create(
            title="Test Ticket",
            description="This is a test ticket.",
            created_by=cls.user,
        )

    def test_card_serializer_includes_expected_fields(self):
        serializer = TicketCardSerializer(self.ticket)

        self.assertEqual(serializer.data["title"], "Test Ticket")
        self.assertEqual(serializer.data["display_id"], self.ticket.display_id)
        self.assertEqual(serializer.data["status"], Ticket.Status.OPEN)
        self.assertEqual(serializer.data["status_display"], "Open")
        self.assertEqual(serializer.data["priority"], Ticket.Priority.MEDIUM)
        self.assertEqual(serializer.data["priority_display"], "Medium")

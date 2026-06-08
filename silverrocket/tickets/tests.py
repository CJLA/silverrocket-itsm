from accounts.models import CustomUser
from django.test import TestCase

from tickets.models import Ticket


class TicketModelTests(TestCase):
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

    def test_ticket_creation(self):
        self.assertEqual(self.ticket.title, "Test Ticket")
        self.assertEqual(self.ticket.description, "This is a test ticket.")
        self.assertEqual(self.ticket.status, Ticket.Status.OPEN)
        self.assertEqual(self.ticket.priority, Ticket.Priority.MEDIUM)
        self.assertEqual(self.ticket.created_by, self.user)
        self.assertIsNone(self.ticket.assigned_to)

    def test_string_representation_returns_title(self):
        self.assertEqual(str(self.ticket), "Test Ticket (Open)")

    def test_ticket_can_be_assigned_to_user(self):
        self.ticket.assigned_to = self.user
        self.ticket.save()

        self.assertEqual(self.ticket.assigned_to, self.user)

    def test_ticket_status_can_be_updated(self):
        self.ticket.status = Ticket.Status.IN_PROGRESS
        self.ticket.save()

        self.assertEqual(self.ticket.status, Ticket.Status.IN_PROGRESS)

    def test_ticket_priority_can_be_updated(self):
        self.ticket.priority = Ticket.Priority.HIGH
        self.ticket.save()

        self.assertEqual(self.ticket.priority, Ticket.Priority.HIGH)

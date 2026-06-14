from accounts.models import CustomUser
from rest_framework import status
from rest_framework.test import APITestCase

from tickets.models import Ticket


class TicketURLTests(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email="tech@example.com",
            password="testpass123",
        )
        self.client.force_authenticate(user=self.user)

    def test_ticket_list_endpoint_returns_tickets(self):
        Ticket.objects.create(
            title="Printer Issue",
            description="Printer is jammed.",
            created_by=self.user,
        )

        response = self.client.get("/api/tickets/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Printer Issue")

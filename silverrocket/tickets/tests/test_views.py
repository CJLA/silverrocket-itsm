from accounts.models import CustomUser
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from tickets.models import Ticket


class TicketViewSetTests(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email="tech@example.com",
            password="testpass123",
        )
        self.client.force_authenticate(user=self.user)

    def test_ticket_list_returns_tickets_in_descending_order(self):
        ticket1 = Ticket.objects.create(  # noqa: F841
            title="First Ticket",
            description="Printer is jammed.",
            created_by=self.user,
        )
        ticket2 = Ticket.objects.create(  # noqa: F841
            title="Second Ticket",
            description="Screen is flickering.",
            created_by=self.user,
        )

        response = self.client.get(reverse("tickets:ticket-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["title"], "Second Ticket")
        self.assertEqual(response.data[1]["title"], "First Ticket")

    def test_ticket_creation_sets_created_by(self):
        response = self.client.post(
            reverse("tickets:ticket-list"),
            {
                "title": "New Ticket",
                "description": "Keyboard not working.",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        ticket = Ticket.objects.get()
        self.assertEqual(ticket.title, "New Ticket")
        self.assertEqual(ticket.description, "Keyboard not working.")
        self.assertEqual(ticket.created_by, self.user)


class TicketAuthenticationTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = CustomUser.objects.create_user(
            email="user@example.com",
            password="testpass123",
        )

    def test_ticket_list_requires_authentication(self):
        response = self.client.get(reverse("tickets:ticket-list"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_ticket_creation_requires_authentication(self):
        response = self.client.post(
            reverse("tickets:ticket-list"),
            {
                "title": "Unauthorized Ticket",
                "description": "This should not be created.",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_user_can_access_ticket_list(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse("tickets:ticket-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

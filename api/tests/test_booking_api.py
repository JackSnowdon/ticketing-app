from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from tickets.models import Booking
from tickets.tests.factories import create_event_with_tickets, create_user


class BookingAPITests(APITestCase):
    def setUp(self):
        self.user = create_user()
        self.client.force_authenticate(user=self.user)

        self.event, self.standard, self.vip = create_event_with_tickets()
        self.url = reverse("booking-list")

    def test_authenticated_user_can_create_booking(self):
        response = self.client.post(
            self.url,
            {
                "ticket_type_id": self.standard.id,
                "quantity": 2,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Booking.objects.count(), 1)
        self.assertEqual(response.data["status"], "pending")
        self.assertEqual(len(response.data["items"]), 1)

    def test_unauthenticated_user_cannot_create_booking(self):
        self.client.force_authenticate(user=None)

        response = self.client.post(
            self.url,
            {
                "ticket_type_id": self.standard.id,
                "quantity": 1,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_invalid_ticket_type_returns_404(self):
        response = self.client.post(
            self.url,
            {
                "ticket_type_id": 999999,
                "quantity": 1,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_insufficient_tickets_returns_400(self):
        response = self.client.post(
            self.url,
            {
                "ticket_type_id": self.vip.id,
                "quantity": 3,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Not enough tickets", response.data["detail"])
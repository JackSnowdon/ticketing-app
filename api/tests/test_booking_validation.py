from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from tickets.tests.factories import create_event_with_tickets, create_user


class BookingValidationTests(APITestCase):
    def setUp(self):
        self.user = create_user()
        self.client.force_authenticate(user=self.user)

        self.url = reverse("booking-list")
        self.event, self.standard, self.vip = create_event_with_tickets()

    def test_valid_booking_returns_201(self):
        payload = {
            "ticket_type_id": self.standard.id,
            "quantity": 2,
        }

        response = self.client.post(self.url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data["items"]), 1)
        self.assertEqual(response.data["items"][0]["quantity"], 2)

    def test_zero_quantity_is_rejected(self):
        payload = {
            "ticket_type_id": self.standard.id,
            "quantity": 0,
        }

        response = self.client.post(self.url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("quantity", response.data)

    def test_negative_quantity_is_rejected(self):
        payload = {
            "ticket_type_id": self.standard.id,
            "quantity": -1,
        }

        response = self.client.post(self.url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("quantity", response.data)

    def test_unknown_ticket_type_is_rejected(self):
        payload = {
            "ticket_type_id": 433123,  # Assuming this ID does not exist
            "quantity": 1,
        }

        response = self.client.post(self.url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("ticket_type_id", response.data)

    def test_quantity_above_max_per_booking_is_rejected(self):
        payload = {
            "ticket_type_id": self.standard.id,
            "quantity": self.standard.max_per_booking + 1,
        }

        response = self.client.post(self.url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("quantity", response.data)

    def test_anonymous_user_cannot_create_booking(self):
        self.client.force_authenticate(user=None)

        payload = {
            "ticket_type_id": self.standard.id,
            "quantity": 1,
        }

        response = self.client.post(self.url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from tickets.models import Booking, TicketType
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

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_invalid_ticket_type_returns_400(self):
        payload = {
        "ticket_type_id": 433123,  # Assuming this ID does not exist
        "quantity": 1,
        }

        response = self.client.post(self.url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("ticket_type_id", response.data)

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

    def test_quantity_above_available_tickets_is_rejected(self):
        ticket_type = TicketType.objects.create(
            event=self.event,
            name="Limited",
            price=30,
            quantity_total=2,
            quantity_available=2,
            max_per_booking=10,
        )

        payload = {
            "ticket_type_id": ticket_type.id,
            "quantity": 3,
        }

        response = self.client.post(self.url, payload, format="json")
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("detail", response.data)
        self.assertEqual(
            response.data["detail"],
            "Not enough tickets are available for this booking.",
        )


class BookingAPIAuthenticationTests(APITestCase):
    def setUp(self):
        self.user = create_user()
        self.other_user = create_user(username="otheruser")
        self.event, self.standard, self.vip = create_event_with_tickets()

    def authenticate(self, user):
        response = self.client.post(
            "/api/auth/token/",
            {
                "username": user.username,
                "password": "testpass123",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        token = response.data["access"]
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {token}"
        )

    def test_unauthenticated_user_cannot_create_booking(self):
        response = self.client.post(
            "/api/bookings/",
            {
                "ticket_type_id": self.standard.id,
                "quantity": 1,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_authenticated_user_can_create_booking(self):
        self.authenticate(self.user)

        response = self.client.post(
            "/api/bookings/",
            {
                "ticket_type_id": self.standard.id,
                "quantity": 2,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )
        self.assertEqual(response.data["status"], "pending")
        self.assertEqual(len(response.data["items"]), 1)

    def test_user_only_sees_their_own_bookings(self):
        self.authenticate(self.user)

        own_booking_response = self.client.post(
            "/api/bookings/",
            {
                "ticket_type_id": self.standard.id,
                "quantity": 1,
            },
            format="json",
        )

        self.assertEqual(
            own_booking_response.status_code,
            status.HTTP_201_CREATED,
        )

        other_booking_response = self.client.post(
            "/api/bookings/",
            {
                "ticket_type_id": self.standard.id,
                "quantity": 1,
            },
            format="json",
        )

        # This request is still authenticated as self.user,
        # so both bookings belong to self.user. We use it to
        # ensure the list endpoint returns user-scoped results.
        self.assertEqual(
            other_booking_response.status_code,
            status.HTTP_201_CREATED,
        )

        list_response = self.client.get("/api/bookings/")

        self.assertEqual(
            list_response.status_code,
            status.HTTP_200_OK,
        )

        references = {
            booking["reference"]
            for booking in list_response.data["results"]
        }

        self.assertEqual(len(references), 2)

    def test_user_cannot_retrieve_another_users_booking(self):
        self.authenticate(self.user)

        booking_response = self.client.post(
            "/api/bookings/",
            {
                "ticket_type_id": self.standard.id,
                "quantity": 1,
            },
            format="json",
        )

        booking_reference = booking_response.data["reference"]

        self.client.credentials()

        self.authenticate(self.other_user)

        response = self.client.get(
            f"/api/bookings/{booking_reference}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    def test_user_cannot_cancel_another_users_booking(self):
        self.authenticate(self.user)

        booking_response = self.client.post(
            "/api/bookings/",
            {
                "ticket_type_id": self.standard.id,
                "quantity": 1,
            },
            format="json",
        )

        booking_reference = booking_response.data["reference"]

        self.client.credentials()

        self.authenticate(self.other_user)

        response = self.client.post(
            f"/api/bookings/{booking_reference}/cancel/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )
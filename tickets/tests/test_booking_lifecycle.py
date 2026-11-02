from django.test import TestCase

from tickets.exceptions import TicketingError
from tickets.models import Booking
from tickets.services.bookings import (
    cancel_booking,
    create_booking,
    get_user_booking,
)
from tickets.tests.factories import create_event_with_tickets, create_user


class BookingLifecycleServiceTests(TestCase):
    def setUp(self):
        self.user = create_user()
        self.other_user = create_user(username="otheruser")

        self.event, self.standard, self.vip = create_event_with_tickets(
            standard_available=10,
        )

    def test_user_can_retrieve_their_own_booking(self):
        booking = create_booking(
            user=self.user,
            ticket_type_id=self.standard.id,
            quantity=2,
        )

        retrieved = get_user_booking(
            user=self.user,
            reference=booking.reference,
        )

        self.assertEqual(retrieved.id, booking.id)

    def test_user_cannot_retrieve_another_users_booking(self):
        booking = create_booking(
            user=self.user,
            ticket_type_id=self.standard.id,
            quantity=2,
        )

        with self.assertRaises(Booking.DoesNotExist):
            get_user_booking(
                user=self.other_user,
                reference=booking.reference,
            )

    def test_cancelling_pending_booking_returns_tickets(self):
        booking = create_booking(
            user=self.user,
            ticket_type_id=self.standard.id,
            quantity=2,
        )

        self.standard.refresh_from_db()
        self.assertEqual(self.standard.quantity_available, 8)

        cancelled_booking = cancel_booking(
            user=self.user,
            reference=booking.reference,
        )

        self.assertEqual(
            cancelled_booking.status,
            Booking.Status.CANCELLED,
        )

        self.standard.refresh_from_db()
        self.assertEqual(self.standard.quantity_available, 10)

    def test_cannot_cancel_another_users_booking(self):
        booking = create_booking(
            user=self.user,
            ticket_type_id=self.standard.id,
            quantity=2,
        )

        with self.assertRaises(Booking.DoesNotExist):
            cancel_booking(
                user=self.other_user,
                reference=booking.reference,
            )

    def test_cannot_cancel_booking_twice(self):
        booking = create_booking(
            user=self.user,
            ticket_type_id=self.standard.id,
            quantity=2,
        )

        cancel_booking(
            user=self.user,
            reference=booking.reference,
        )

        with self.assertRaises(TicketingError):
            cancel_booking(
                user=self.user,
                reference=booking.reference,
            )
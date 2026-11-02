from django.test import TestCase

from tickets.exceptions import (
    EventNotPublishedError,
    InsufficientTicketsError,
    InvalidQuantityError,
)
from tickets.models import Booking
from tickets.services.bookings import create_booking
from tickets.tests.factories import create_event_with_tickets, create_user


class CreateBookingServiceTests(TestCase):
    def setUp(self):
        self.user = create_user()
        self.event, self.standard, self.vip = create_event_with_tickets()

    def test_creates_pending_booking_and_reduces_availability(self):
        booking = create_booking(
            user=self.user,
            ticket_type_id=self.standard.id,
            quantity=2,
        )

        self.assertEqual(booking.status, Booking.Status.PENDING)
        self.assertEqual(booking.items.count(), 1)
        self.assertEqual(booking.items.first().quantity, 2)

        self.standard.refresh_from_db()
        self.assertEqual(self.standard.quantity_available, 8)

    def test_rejects_zero_quantity(self):
        with self.assertRaises(InvalidQuantityError):
            create_booking(
                user=self.user,
                ticket_type_id=self.standard.id,
                quantity=0,
            )

    def test_rejects_negative_quantity(self):
        with self.assertRaises(InvalidQuantityError):
            create_booking(
                user=self.user,
                ticket_type_id=self.standard.id,
                quantity=-1,
            )

    def test_rejects_quantity_above_max_per_booking(self):
        with self.assertRaises(InvalidQuantityError):
            create_booking(
                user=self.user,
                ticket_type_id=self.standard.id,
                quantity=5,
            )

    def test_rejects_insufficient_tickets(self):
        with self.assertRaises(InsufficientTicketsError):
            create_booking(
                user=self.user,
                ticket_type_id=self.vip.id,
                quantity=3,
            )

    def test_rejects_unpublished_event(self):
        self.event.is_published = False
        self.event.save()

        with self.assertRaises(EventNotPublishedError):
            create_booking(
                user=self.user,
                ticket_type_id=self.standard.id,
                quantity=1,
            )

    def test_generates_unique_references(self):
        first = create_booking(
            user=self.user,
            ticket_type_id=self.standard.id,
            quantity=1,
        )
        second = create_booking(
            user=self.user,
            ticket_type_id=self.standard.id,
            quantity=1,
        )

        self.assertNotEqual(first.reference, second.reference)
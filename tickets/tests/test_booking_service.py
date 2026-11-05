from django.test import TestCase
from django.utils import timezone

from tickets.exceptions import (
    EventNotPublishedError,
    InsufficientTicketsError,
    InvalidQuantityError,
    TicketingError,
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


class CreateBookingBoundaryTests(TestCase):
    def setUp(self):
        self.user = create_user()
        self.event, self.standard, self.vip = create_event_with_tickets()

    def test_allows_booking_exact_max_per_booking(self):
        booking = create_booking(
            user=self.user,
            ticket_type_id=self.standard.id,
            quantity=4,
        )

        self.assertEqual(booking.items.first().quantity, 4)

        self.standard.refresh_from_db()
        self.assertEqual(self.standard.quantity_available, 6)

    def test_allows_booking_final_available_ticket(self):
        self.standard.quantity_available = 1
        self.standard.save(update_fields=["quantity_available"])

        booking = create_booking(
            user=self.user,
            ticket_type_id=self.standard.id,
            quantity=1,
        )

        self.standard.refresh_from_db()
        self.assertEqual(self.standard.quantity_available, 0)
        self.assertEqual(booking.status, Booking.Status.PENDING)

    def test_rejects_booking_more_than_remaining_availability(self):
        self.standard.quantity_available = 1
        self.standard.save(update_fields=["quantity_available"])

        with self.assertRaises(InsufficientTicketsError):
            create_booking(
                user=self.user,
                ticket_type_id=self.standard.id,
                quantity=2,
            )

        self.standard.refresh_from_db()
        self.assertEqual(self.standard.quantity_available, 1)

    def test_rejects_nonexistent_ticket_type(self):
        with self.assertRaises(TicketingError):
            create_booking(
                user=self.user,
                ticket_type_id=999999,
                quantity=1,
            )

    def test_rejects_booking_after_event_has_started(self):
        self.event.starts_at = timezone.now() - timezone.timedelta(hours=1)
        self.event.save(update_fields=["starts_at"])

        with self.assertRaises(EventNotPublishedError):
            create_booking(
                user=self.user,
                ticket_type_id=self.standard.id,
                quantity=1,
            )

    def test_failed_booking_does_not_reduce_availability(self):
        with self.assertRaises(InsufficientTicketsError):
            create_booking(
                user=self.user,
                ticket_type_id=self.vip.id,
                quantity=3,
            )

        self.vip.refresh_from_db()
        self.assertEqual(self.vip.quantity_available, 2)
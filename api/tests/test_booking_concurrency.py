from concurrent.futures import ThreadPoolExecutor

from django.db import close_old_connections, connection, transaction
from django.test import TransactionTestCase

from tickets.exceptions import InsufficientTicketsError
from tickets.services.bookings import create_booking
from tickets.tests.factories import create_event_with_tickets, create_user


class BookingConcurrencyTests(TransactionTestCase):
    def setUp(self):
        self.user = create_user()
        self.event, self.standard, self.vip = create_event_with_tickets(
            standard_available=1,
        )

    def tearDown(self):
        close_old_connections()
        connection.close()

    def test_cannot_oversell_last_ticket(self):
        def attempt_booking():
            connection.close()

            try:
                create_booking(
                    user=self.user,
                    ticket_type_id=self.standard.id,
                    quantity=1,
                )
                return "success"
            except InsufficientTicketsError:
                return "rejected"
            finally:
                connection.close()

        with ThreadPoolExecutor(max_workers=2) as executor:
            results = list(executor.map(lambda _: attempt_booking(), range(2)))

        self.standard.refresh_from_db()

        self.assertEqual(results.count("success"), 1)
        self.assertEqual(results.count("rejected"), 1)
        self.assertEqual(self.standard.quantity_available, 0)
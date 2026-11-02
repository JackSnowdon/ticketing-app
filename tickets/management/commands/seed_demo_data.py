from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from tickets.models import Event, TicketType, Venue


class Command(BaseCommand):
    help = "Create public demo venues, events, and ticket types."

    def handle(self, *args, **options):
        now = timezone.now()

        venues = {
            "kks-steel-mill": self.get_or_create_venue(
                name="KK's Steel Mill",
                city="Wolverhampton",
                address="South Street, Wolverhampton",
            ),
            "o2-academy": self.get_or_create_venue(
                name="O2 Academy",
                city="Birmingham",
                address="52-54 Bristol Street, Birmingham",
            ),
            "the-halls": self.get_or_create_venue(
                name="The Halls",
                city="Wolverhampton",
                address="North Street, Wolverhampton",
            ),
        }

        events = [
            {
                "title": "Indie Rock Night",
                "description": "An evening of local and touring indie rock bands.",
                "venue": venues["kks-steel-mill"],
                "starts_at": now + timedelta(days=7),
                "doors_open_at": now + timedelta(days=7, hours=-1),
                "ticket_types": [
                    ("Standard", 22.50, 120, 4),
                    ("VIP", 45.00, 20, 2),
                ],
            },
            {
                "title": "Acoustic Sessions",
                "description": "Intimate acoustic performances from emerging artists.",
                "venue": venues["the-halls"],
                "starts_at": now + timedelta(days=14),
                "doors_open_at": now + timedelta(days=14, hours=-1),
                "ticket_types": [
                    ("Standard", 18.00, 80, 4),
                    ("Balcony", 28.00, 30, 4),
                ],
            },
            {
                "title": "Electronic Showcase",
                "description": "A night of electronic music, visuals, and late DJs.",
                "venue": venues["o2-academy"],
                "starts_at": now + timedelta(days=21),
                "doors_open_at": now + timedelta(days=21, hours=-2),
                "ticket_types": [
                    ("Standard", 27.50, 250, 6),
                    ("VIP", 65.00, 40, 4),
                ],
            },
            {
                "title": "Comedy Night",
                "description": "A stand-up comedy showcase featuring regional acts.",
                "venue": venues["kks-steel-mill"],
                "starts_at": now + timedelta(days=28),
                "doors_open_at": now + timedelta(days=28, hours=-1),
                "ticket_types": [
                    ("Standard", 16.00, 100, 4),
                ],
            },
            {
                "title": "Jazz & Soul Evening",
                "description": "Live jazz, soul, and Motown classics.",
                "venue": venues["the-halls"],
                "starts_at": now + timedelta(days=35),
                "doors_open_at": now + timedelta(days=35, hours=-1),
                "ticket_types": [
                    ("Standard", 24.00, 90, 4),
                    ("VIP", 48.00, 15, 2),
                ],
            },
        ]

        created_events = 0
        created_ticket_types = 0

        for event_data in events:
            ticket_types = event_data.pop("ticket_types")

            event, event_created = Event.objects.get_or_create(
                title=event_data["title"],
                venue=event_data["venue"],
                defaults=event_data,
            )

            if event_created:
                event.is_published = True
                event.save()
                created_events += 1

            for name, price, quantity, max_per_booking in ticket_types:
                _, ticket_created = TicketType.objects.get_or_create(
                    event=event,
                    name=name,
                    defaults={
                        "price": price,
                        "quantity_total": quantity,
                        "quantity_available": quantity,
                        "max_per_booking": max_per_booking,
                    },
                )

                if ticket_created:
                    created_ticket_types += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Seed complete: {created_events} events and "
                f"{created_ticket_types} ticket types created."
            )
        )

    def get_or_create_venue(self, *, name, city, address):
        venue, _ = Venue.objects.get_or_create(
            name=name,
            city=city,
            defaults={"address": address},
        )

        return venue
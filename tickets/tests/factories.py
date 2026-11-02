from datetime import date

from django.contrib.auth import get_user_model
from django.utils import timezone

from accounts.models import Address
from tickets.models import Event, TicketType, Venue

User = get_user_model()


def create_user(
    username="testuser",
    password="testpass123",
    email=None,
    date_of_birth=None,
    address_data=None,
):
    if email is None:
        email = f"{username}@example.com"

    if date_of_birth is None:
        date_of_birth = date(1995, 1, 1)

    user = User.objects.create_user(
        username=username,
        email=email,
        password=password,
        date_of_birth=date_of_birth,
    )

    if address_data is not None:
        Address.objects.create(user=user, **address_data)

    return user


def create_event_with_tickets(
    *,
    standard_available=10,
    vip_available=2,
    starts_in_days=7,
):
    venue = Venue.objects.create(
        name="Test Venue",
        city="Wolverhampton",
    )

    event = Event.objects.create(
        title="Test Event",
        venue=venue,
        starts_at=timezone.now() + timezone.timedelta(days=starts_in_days),
        is_published=True,
    )

    standard = TicketType.objects.create(
        event=event,
        name="Standard",
        price=25,
        quantity_total=standard_available,
        quantity_available=standard_available,
        max_per_booking=4,
    )

    vip = TicketType.objects.create(
        event=event,
        name="VIP",
        price=45,
        quantity_total=vip_available,
        quantity_available=vip_available,
        max_per_booking=5,
    )

    return event, standard, vip
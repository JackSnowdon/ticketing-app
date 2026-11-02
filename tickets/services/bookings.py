import uuid

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.utils import timezone

from tickets.exceptions import (
    EventNotPublishedError,
    InsufficientTicketsError,
    InvalidQuantityError,
    TicketingError,
)
from tickets.models import Booking, BookingItem, TicketType


def generate_booking_reference():
    return uuid.uuid4().hex[:12].upper()


@transaction.atomic
def create_booking(*, user, ticket_type_id: int, quantity: int) -> Booking:
    if quantity <= 0:
        raise InvalidQuantityError("Booking quantity must be greater than zero.")

    try:
        ticket_type = (
            TicketType.objects
            .select_for_update()
            .select_related("event")
            .get(pk=ticket_type_id)
        )
    except ObjectDoesNotExist as exc:
        raise TicketingError("Ticket type not found.") from exc

    event = ticket_type.event

    if not event.is_published:
        raise EventNotPublishedError("This event is not available for booking.")

    if event.starts_at <= timezone.now():
        raise EventNotPublishedError("This event has already started.")

    if quantity > ticket_type.max_per_booking:
        raise InvalidQuantityError(
            f"You can book a maximum of {ticket_type.max_per_booking} "
            f"{ticket_type.name} tickets."
        )

    if ticket_type.quantity_available < quantity:
        raise InsufficientTicketsError(
            "Not enough tickets are available for this booking."
        )

    ticket_type.quantity_available -= quantity
    ticket_type.save(update_fields=["quantity_available"])

    booking = Booking.objects.create(
        user=user,
        reference=generate_booking_reference(),
        status=Booking.Status.PENDING,
    )

    BookingItem.objects.create(
        booking=booking,
        ticket_type=ticket_type,
        quantity=quantity,
        unit_price=ticket_type.price,
    )

    return booking


def get_user_booking(*, user, reference: str) -> Booking:
    try:
        return (
            Booking.objects
            .prefetch_related("items__ticket_type__event")
            .get(
                reference=reference,
                user=user,
            )
        )
    except Booking.DoesNotExist as exc:
        raise Booking.DoesNotExist("Booking not found.") from exc


@transaction.atomic
def cancel_booking(*, user, reference: str) -> Booking:
    try:
        booking = (
            Booking.objects
            .select_for_update()
            .prefetch_related("items__ticket_type")
            .get(
                reference=reference,
                user=user,
            )
        )
    except Booking.DoesNotExist as exc:
        raise Booking.DoesNotExist("Booking not found.") from exc

    if booking.status == Booking.Status.CANCELLED:
        raise TicketingError("This booking has already been cancelled.")

    if booking.status == Booking.Status.CONFIRMED:
        raise TicketingError("Confirmed bookings cannot be cancelled.")

    for item in booking.items.all():
        ticket_type = (
            TicketType.objects
            .select_for_update()
            .get(pk=item.ticket_type_id)
        )

        ticket_type.quantity_available += item.quantity
        ticket_type.save(update_fields=["quantity_available"])

    booking.status = Booking.Status.CANCELLED
    booking.save(update_fields=["status", "updated_at"])

    return booking
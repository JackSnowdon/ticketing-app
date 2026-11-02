from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics, permissions, status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from api.serializers.bookings import (
    BookingSerializer,
    CreateBookingSerializer,
)
from tickets.exceptions import TicketingError
from tickets.models import Booking
from tickets.services.bookings import (
    cancel_booking,
    create_booking,
    get_user_booking,
)


class BookingListCreateAPIView(generics.ListCreateAPIView):
    """Handles GET /api/bookings/ and POST /api/bookings/."""

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BookingSerializer

    def get_queryset(self):
        return (
            Booking.objects
            .filter(user=self.request.user)
            .prefetch_related("items__ticket_type__event")
        )

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CreateBookingSerializer

        return BookingSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            booking = create_booking(
                user=request.user,
                ticket_type_id=serializer.validated_data["ticket_type_id"],
                quantity=serializer.validated_data["quantity"],
            )
        except TicketingError as exc:
            if str(exc) == "Ticket type not found.":
                raise NotFound(str(exc))

            return Response(
                {"detail": str(exc)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        output = BookingSerializer(booking)
        return Response(output.data, status=status.HTTP_201_CREATED)


class BookingDetailAPIView(generics.RetrieveAPIView):
    """Handles GET /api/bookings/<reference>/."""

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BookingSerializer

    def get_object(self):
        try:
            return get_user_booking(
                user=self.request.user,
                reference=self.kwargs["reference"],
            )
        except Booking.DoesNotExist as exc:
            raise NotFound("Booking not found.") from exc


class BookingCancelAPIView(generics.GenericAPIView):
    """Handles POST /api/bookings/<reference>/cancel/."""

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BookingSerializer

    def post(self, request, *args, **kwargs):
        try:
            booking = cancel_booking(
                user=request.user,
                reference=self.kwargs["reference"],
            )
        except Booking.DoesNotExist as exc:
            raise NotFound("Booking not found.") from exc
        except TicketingError as exc:
            return Response(
                {"detail": str(exc)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        output = BookingSerializer(booking)
        return Response(output.data, status=status.HTTP_200_OK)
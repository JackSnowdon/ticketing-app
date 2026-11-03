from rest_framework import serializers

from tickets.models import Booking, BookingItem, TicketType


class BookingItemSerializer(serializers.ModelSerializer):
    ticket_type_name = serializers.CharField(
        source="ticket_type.name",
        read_only=True,
    )
    event_title = serializers.CharField(
        source="ticket_type.event.title",
        read_only=True,
    )
    line_total = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True,
    )   
    event_id = serializers.IntegerField(
        source="ticket_type.event.id",
        read_only=True
    )

    class Meta:
        model = BookingItem
        fields = [
            "id",
            "event_id",
            "ticket_type",
            "ticket_type_name",
            "event_title",
            "quantity",
            "unit_price",
            "line_total",
        ]


class BookingSerializer(serializers.ModelSerializer):
    items = BookingItemSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField()

    class Meta:
        model = Booking
        fields = [
            "id",
            "reference",
            "status",
            "created_at",
            "updated_at",
            "items",
            "total",
        ]

    def get_total(self, obj):
        return sum(item.line_total for item in obj.items.all())


class CreateBookingSerializer(serializers.Serializer):
    ticket_type_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)

    def validate_ticket_type_id(self, value):
        if not TicketType.objects.filter(id=value).exists():
            raise serializers.ValidationError(
                "Ticket type not found."
            )

        return value

    def validate(self, data):
        ticket_type_id = data.get("ticket_type_id")
        quantity = data.get("quantity")

        if ticket_type_id is None or quantity is None:
            return data

        try:
            ticket_type = TicketType.objects.get(id=ticket_type_id)
        except TicketType.DoesNotExist:
            return data

        if quantity > ticket_type.max_per_booking:
            raise serializers.ValidationError(
                {
                    "quantity": (
                        f"You can book a maximum of "
                        f"{ticket_type.max_per_booking} "
                        f"{ticket_type.name} tickets per booking."
                    )
                }
            )

        return data
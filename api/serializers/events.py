from rest_framework import serializers

from tickets.models import Event, TicketType, Venue


class VenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venue
        fields = ["id", "name", "city"]


class TicketTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketType
        fields = [
            "id",
            "name",
            "price",
            "quantity_available",
            "max_per_booking",
        ]


class EventSerializer(serializers.ModelSerializer):
    venue = VenueSerializer(read_only=True)
    ticket_types = TicketTypeSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = [
            "id",
            "title",
            "description",
            "venue",
            "starts_at",
            "doors_open_at",
            "is_published",
            "ticket_types",
        ]


class EventListSerializer(serializers.ModelSerializer):
    venue = VenueSerializer(read_only=True)

    class Meta:
        model = Event
        fields = [
            "id",
            "title",
            "venue",
            "starts_at",
            "doors_open_at",
            "is_published",
        ]
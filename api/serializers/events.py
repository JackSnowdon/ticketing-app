from django.utils import timezone
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

    def validate_title(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Event title cannot be blank."
            )

        return value

    def validate_starts_at(self, value):
        if value <= timezone.now():
            raise serializers.ValidationError(
                "Event start time must be in the future."
            )

        return value


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
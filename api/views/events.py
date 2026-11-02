from django.utils import timezone
from rest_framework import generics

from api.serializers.events import EventListSerializer, EventSerializer
from tickets.models import Event


class EventListAPIView(generics.ListAPIView):
    serializer_class = EventListSerializer

    def get_queryset(self):
        now = timezone.now()

        return (
            Event.objects.filter(
                is_published=True,
                starts_at__gte=now,
            )
            .select_related("venue")
            .prefetch_related("ticket_types")
        )


class EventDetailAPIView(generics.RetrieveAPIView):
    serializer_class = EventSerializer

    def get_queryset(self):
        now = timezone.now()

        return (
            Event.objects.filter(is_published=True)
            .select_related("venue")
            .prefetch_related("ticket_types")
        )
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import OrderingFilter, SearchFilter

from api.filters.events import EventFilter
from api.serializers.events import EventListSerializer, EventSerializer
from tickets.models import Event


class EventListAPIView(generics.ListAPIView):
    serializer_class = EventListSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = EventFilter
    search_fields = ["title", "description", "venue__name", "venue__city"]
    ordering_fields = ["starts_at", "title"]
    ordering = ["starts_at"]

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
        return (
            Event.objects.filter(is_published=True)
            .select_related("venue")
            .prefetch_related("ticket_types")
        )
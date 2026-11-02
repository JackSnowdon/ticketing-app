from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from tickets.tests.factories import create_event_with_tickets


class EventFilteringTests(APITestCase):
    def setUp(self):
        self.url = reverse("event-list")
        self.event, self.standard, self.vip = create_event_with_tickets()

    def test_can_search_events_by_title(self):
        response = self.client.get(self.url, {"search": "Test Event"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_search_with_no_match_returns_empty_results(self):
        response = self.client.get(self.url, {"search": "no-such-event"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 0)

    def test_can_order_events_by_title(self):
        response = self.client.get(self.url, {"ordering": "title"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        titles = [event["title"] for event in response.data["results"]]
        self.assertEqual(titles, sorted(titles))

    def test_can_filter_by_city(self):
        response = self.client.get(
            self.url,
            {"city": self.event.venue.city},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_can_filter_by_venue_slug(self):
        response = self.client.get(
            self.url,
            {"venue": self.event.venue.slug},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
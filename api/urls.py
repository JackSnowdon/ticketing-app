from django.urls import path

from api.views.bookings import (
    BookingCancelAPIView,
    BookingDetailAPIView,
    BookingListCreateAPIView,
)
from api.views.events import EventDetailAPIView, EventListAPIView

urlpatterns = [
    path("events/", EventListAPIView.as_view(), name="event-list"),
    path(
        "events/<int:pk>/",
        EventDetailAPIView.as_view(),
        name="event-detail",
    ),

    path("bookings/", BookingListCreateAPIView.as_view(), name="booking-list"),
    path(
        "bookings/<str:reference>/",
        BookingDetailAPIView.as_view(),
        name="booking-detail",
    ),
    path(
        "bookings/<str:reference>/cancel/",
        BookingCancelAPIView.as_view(),
        name="booking-cancel",
    ),
]
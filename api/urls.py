from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from api.views.bookings import (
    BookingCancelAPIView,
    BookingDetailAPIView,
    BookingListCreateAPIView,
)
from api.views.events import EventDetailAPIView, EventListAPIView
from api.views.health import health_check
from api.views.accounts import RegisterAPIView, MeAPIView

urlpatterns = [
    path("health/", health_check, name="health-check"),
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
    path(
        "auth/token/",
        TokenObtainPairView.as_view(),
        name="token-obtain-pair",
    ),
    path(
        "auth/token/refresh/",
        TokenRefreshView.as_view(),
        name="token-refresh",
    ),
    path(
        "auth/register/",
        RegisterAPIView.as_view(),
        name="register",
    ),
    path(
        "auth/me/",
        MeAPIView.as_view(),
        name="me",
    ),
]
from django.urls import path

from api.views.events import EventDetailAPIView, EventListAPIView

urlpatterns = [
    path("events/", EventListAPIView.as_view(), name="event-list"),
    path("events/<int:pk>/", EventDetailAPIView.as_view(), name="event-detail"),
]
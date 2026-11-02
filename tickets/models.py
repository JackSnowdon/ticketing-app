from django.conf import settings
from django.db import models
from django.utils.text import slugify


class Venue(models.Model):
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    slug = models.SlugField(
    max_length=255,
    unique=True,
    blank=True,
    )
    address = models.TextField(blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name}, {self.city}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)


class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    venue = models.ForeignKey(
        Venue,
        on_delete=models.PROTECT,
        related_name="events",
    )
    starts_at = models.DateTimeField()
    doors_open_at = models.DateTimeField(null=True, blank=True)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["starts_at"]
        indexes = [
            models.Index(fields=["starts_at"]),
            models.Index(fields=["is_published", "starts_at"]),
        ]

    def __str__(self):
        return self.title


class TicketType(models.Model):
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="ticket_types",
    )
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity_total = models.PositiveIntegerField()
    quantity_available = models.PositiveIntegerField()
    max_per_booking = models.PositiveIntegerField(default=4)

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=models.Q(quantity_available__lte=models.F("quantity_total")),
                name="ticket_available_cannot_exceed_total",
            ),
            models.UniqueConstraint(
                fields=["event", "name"],
                name="unique_ticket_type_name_per_event",
            ),
        ]

    def __str__(self):
        return f"{self.event.title} — {self.name}"


class Booking(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        CONFIRMED = "confirmed", "Confirmed"
        CANCELLED = "cancelled", "Cancelled"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="bookings",
    )
    reference = models.CharField(max_length=20, unique=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["user", "status"]),
        ]

    def __str__(self):
        return f"{self.reference} — {self.user}"


class BookingItem(models.Model):
    booking = models.ForeignKey(
        Booking,
        on_delete=models.CASCADE,
        related_name="items",
    )
    ticket_type = models.ForeignKey(
        TicketType,
        on_delete=models.PROTECT,
        related_name="booking_items",
    )
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=models.Q(quantity__gt=0),
                name="booking_item_quantity_must_be_positive",
            ),
        ]

    @property
    def line_total(self):
        return self.unit_price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.ticket_type}"
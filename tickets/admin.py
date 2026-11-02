from django.contrib import admin

from .models import Booking, BookingItem, Event, TicketType, Venue


@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "city"]
    search_fields = ["name", "city"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "venue", "starts_at", "is_published")
    list_filter = ("is_published", "venue")
    search_fields = ("title", "venue__name")
    date_hierarchy = "starts_at"


@admin.register(TicketType)
class TicketTypeAdmin(admin.ModelAdmin):
    list_display = (
        "event",
        "name",
        "price",
        "quantity_total",
        "quantity_available",
        "max_per_booking",
    )
    list_filter = ("event",)


class BookingItemInline(admin.TabularInline):
    model = BookingItem
    extra = 0


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("reference", "user", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("reference", "user__username")
    inlines = [BookingItemInline]
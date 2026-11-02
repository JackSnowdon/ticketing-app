import django_filters

from tickets.models import Event


class EventFilter(django_filters.FilterSet):
    city = django_filters.CharFilter(
        field_name="venue__city",
        lookup_expr="iexact",
    )
    venue = django_filters.CharFilter(
        field_name="venue__slug",
        lookup_expr="iexact",
    )

    class Meta:
        model = Event
        fields = ["city", "venue"]
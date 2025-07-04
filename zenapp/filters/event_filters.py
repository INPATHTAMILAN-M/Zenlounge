from django_filters import rest_framework as filters
from zenapp.models import Event
from django_filters import filters as django_filters
from django.utils import timezone
from datetime import timedelta

class EventFilter(filters.FilterSet):
    is_future = django_filters.BooleanFilter(method='filter_is_future')
    title = django_filters.CharFilter(lookup_expr='icontains')
    end_date = django_filters.DateFilter(lookup_expr='lte')

    class Meta:
        model = Event
        fields = ['title', 'start_date', 'end_date', 'description', 'lounge_type', 
                  'price', 'start_time', 'end_time', 'moderator', 'seat_count', 'is_featured']
    
    def filter_is_future(self, queryset, name, value):
        now = timezone.now()
        if value:
            # Show only events that have a start date in the future, including those that are one day before the event.
            return queryset.filter(start_date__gt=now - timedelta(days=1))
        return queryset


from django_filters import rest_framework as filters
from zenapp.models import Event
from django_filters import filters as django_filters

class EventFilter(filters.FilterSet):
    class Meta:
        model = Event
        fields = ['title','start_date','end_date', 'description', 'title', 
                  'description', 'start_date', 'end_date', 'lounge_type', 
                  'price', 'start_time', 'end_time','moderator','seat_count', 'is_featured']
        
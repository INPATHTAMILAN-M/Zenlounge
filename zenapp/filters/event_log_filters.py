from django_filters import rest_framework as filters
from zenapp.models import EventLog

class EventLogFilter(filters.FilterSet):
    class Meta:
        model = EventLog
        fields = '__all__'

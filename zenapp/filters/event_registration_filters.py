from django_filters import rest_framework as filters
from zenapp.models import EventRegistration

class EventRegistrationFilter(filters.FilterSet):
    registration_date = filters.DateFromToRangeFilter()
    registration_id = filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = EventRegistration
        fields = '__all__'

from django_filters import rest_framework as filters
from ...zenapp.models import EventRegistration

class EventRegistrationFilter(filters.FilterSet):
    class Meta:
        model = EventRegistration
        fields = '__all__'

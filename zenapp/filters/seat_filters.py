from django_filters import rest_framework as filters
from ...zenapp.models import Seat

class SeatFilter(filters.FilterSet):
    class Meta:
        model = Seat
        fields = '__all__'

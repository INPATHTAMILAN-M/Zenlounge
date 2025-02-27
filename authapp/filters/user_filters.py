from django.contrib.auth.models import Group
from django_filters import rest_framework as filters
from ..models import CustomUser

class CustomUserFilter(filters.FilterSet):
    group_name = filters.CharFilter(field_name="groups__name", lookup_expr="icontains")  # Filter by group name

    class Meta:
        model = CustomUser
        fields = {
            'phone_number': ['exact', 'icontains'],
            'address': ['exact', 'icontains'],
            'date_of_birth': ['exact', 'year__gt', 'year__lt'],
            'university': ['exact'],
            'intrested_topics': ['exact'],
            'year_of_entry': ['exact', 'gte', 'lte'],
            'email': ['exact', 'icontains'],
        }

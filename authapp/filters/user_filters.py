from django.contrib.auth.models import Group
from django_filters import rest_framework as filters
from ..models import CustomUser

class CustomUserFilter(filters.FilterSet):
    group_name = filters.CharFilter(field_name="groups__name", lookup_expr="icontains")  # Filter by group name
    is_active = filters.BooleanFilter(field_name="is_active")  # Filter by active status
    search = filters.CharFilter(field_name="username", lookup_expr="icontains")  # Search filter

    class Meta:
        model = CustomUser
        fields = {
            'phone_number': ['exact', 'icontains'],
            'address': ['exact', 'icontains'],
            'date_of_birth': ['exact', 'year__gt', 'year__lt'],
            'university': ['exact'],
            'year_of_entry': ['exact', 'gte', 'lte'],
            'email': ['exact', 'icontains'],
        }

from django_filters import rest_framework as filters
from zenapp.models import CustomerSupport

class CustomerSupportFilter(filters.FilterSet):
    class Meta:
        model = CustomerSupport
        fields = '__all__'

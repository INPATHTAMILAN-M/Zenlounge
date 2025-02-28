from django_filters import rest_framework as filters
from zenapp.models import Payment

class PaymentFilter(filters.FilterSet):
    class Meta:
        model = Payment
        fields = '__all__'

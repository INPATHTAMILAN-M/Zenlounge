from django_filters import rest_framework as filters
from ...zenapp.models import Coupon

class CouponFilter(filters.FilterSet):
    class Meta:
        model = Coupon
        fields = '__all__'

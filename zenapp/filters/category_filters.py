from django_filters import rest_framework as filters
from zenapp.models import Category

class CategoryFilter(filters.FilterSet):
    class Meta:
        model = Category
        fields = '__all__'

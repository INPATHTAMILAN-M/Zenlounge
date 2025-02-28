from rest_framework import viewsets, permissions, filters
from rest_framework.pagination import PageNumberPagination
from ..models import Category
from ..serializers import (
     CategoryCreateSerializer,
     CategoryGetSerializer, 
     CategoryPatchSerializer,
     CategoryListSerializer
)
from ..filters import CategoryFilter

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'post','patch', 'delete']
    filterset_class = CategoryFilter
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.action == 'create':
            return CategoryCreateSerializer
        elif self.action == 'retrieve':
            return CategoryGetSerializer
        elif self.action == 'partial_update':
            return CategoryPatchSerializer
        return CategoryListSerializer

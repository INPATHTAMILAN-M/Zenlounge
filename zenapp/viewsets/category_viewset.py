from rest_framework import viewsets, permissions
from ..models import Category
from ..serializers import (
     CategoryCreateSerializer,
     CategoryGetSerializer, 
     CategoryPatchSerializer,
     CategoryListSerializer
)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'post','patch', 'delete']
    

    def get_serializer_class(self):
        if self.action == 'create':
            return CategoryCreateSerializer
        elif self.action == 'retrieve':
            return CategoryGetSerializer
        elif self.action == 'partial_update':
            return CategoryPatchSerializer
        return CategoryListSerializer

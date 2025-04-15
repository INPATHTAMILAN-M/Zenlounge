from rest_framework import viewsets, permissions
from authapp.models import CustomUser
from ..serializers import (
    CustomUserCreateSerializer, CustomUserUpdateSerializer, 
    CustomUserListSerializer, CustomUserDetailSerializer
)
from ..filters import CustomUserFilter
from django_filters import rest_framework as filters

class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all().exclude(id=2).order_by('-id')
    serializer_class = CustomUserListSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'post', 'patch','delete']
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = CustomUserFilter


    def get_serializer_class(self):
        if self.action == 'list':
            return CustomUserListSerializer
        elif self.action == 'retrieve':
            return CustomUserDetailSerializer
        elif self.action == 'create':
            return CustomUserCreateSerializer
        elif self.action == 'update' or self.action == 'partial_update':
            return CustomUserUpdateSerializer
        return super().get_serializer_class()
    

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return super().destroy(request, *args, **kwargs)
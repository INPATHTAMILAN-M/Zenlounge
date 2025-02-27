from rest_framework import viewsets, permissions
from authapp.models import CustomUser
from ..serializers import CustomUserSerializer
from ..filters import CustomUserFilter
from django_filters import rest_framework as filters

class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'post', 'patch']
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = CustomUserFilter
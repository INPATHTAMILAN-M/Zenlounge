from rest_framework import viewsets, permissions
from authapp.models import CustomUser
from ..serializers import CustomUserSerializer

class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    authentication_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'post', 'patch']

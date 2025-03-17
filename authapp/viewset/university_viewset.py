from rest_framework import viewsets, permissions
from ..models import University, IntrestedTopic
from ..serializers import UniversitySerializer, IntrestedTopicSerializer

class UniversityViewSet(viewsets.ModelViewSet):
    queryset = University.objects.all()
    serializer_class = UniversitySerializer
    # permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'post', 'patch', 'delete']



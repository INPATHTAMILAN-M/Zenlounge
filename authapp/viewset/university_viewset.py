from rest_framework import viewsets, permissions
from ..models import University, IntrestedTopic
from ..serializers import UniversitySerializer, IntrestedTopicSerializer

class UniversityViewSet(viewsets.ModelViewSet):
    queryset = University.objects.all().order_by('name')
    serializer_class = UniversitySerializer
    # permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'post', 'patch', 'delete']

    def list(self, request, *args, **kwargs):
        self.pagination_class = None  # Disable pagination
        return super().list(request, *args, **kwargs)



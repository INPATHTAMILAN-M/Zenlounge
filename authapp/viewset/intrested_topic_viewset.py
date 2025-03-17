from rest_framework import viewsets, permissions
from ..models import  IntrestedTopic
from ..serializers import IntrestedTopicSerializer

class IntrestedTopicViewSet(viewsets.ModelViewSet):
    queryset = IntrestedTopic.objects.all()
    serializer_class = IntrestedTopicSerializer
    # permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'post', 'patch', 'delete']
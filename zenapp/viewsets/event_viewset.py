from rest_framework import viewsets, permissions
from ..models import Event
from ..serializers.event_serializer import (
    EventCreateSerializer,
    EventGetSerializer,
    EventListSerializer,
    EventPatchSerializer,
)

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventListSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'post','patch', 'delete']

    def get_serializer_class(self):
        if self.action == 'create':
            return EventCreateSerializer
        elif self.action == 'retrieve':
            return EventGetSerializer
        elif self.action == 'update' or self.action == 'partial_update':
            return EventPatchSerializer
        return EventListSerializer

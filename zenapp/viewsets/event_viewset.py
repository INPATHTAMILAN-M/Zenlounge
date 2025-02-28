from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend
from ..filters.event_filters import EventFilter
from ..models import Event
from ..serializers.event_serializer import (
    EventCreateSerializer,
    EventGetSerializer,
    EventListSerializer,
    EventPatchSerializer,
)

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all().order_by('-id')
    serializer_class = EventListSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = EventFilter
    http_method_names = ['get', 'post','patch', 'delete']

    def get_serializer_class(self):
        if self.action == 'create':
            return EventCreateSerializer
        elif self.action == 'retrieve':
            return EventGetSerializer
        elif self.action == 'update' or self.action == 'partial_update':
            return EventPatchSerializer
        return EventListSerializer
    

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
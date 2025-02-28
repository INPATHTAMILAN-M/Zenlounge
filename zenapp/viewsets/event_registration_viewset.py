from rest_framework import viewsets, permissions, filters
from ..models import EventRegistration
from ..serializers.event_registration_serializer import EventRegistrationGetSerializer, EventRegistrationCreateSerializer, EventRegistrationPatchSerializer, EventRegistrationListSerializer
from ..filters import EventRegistrationFilter

class EventRegistrationViewSet(viewsets.ModelViewSet):
    queryset = EventRegistration.objects.all()
    serializer_class = EventRegistrationListSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'post','patch', 'delete']
    filterset_class = EventRegistrationFilter

    def get_serializer_class(self):
        if self.action == 'list':
            return EventRegistrationListSerializer
        elif self.action == 'create':
            return EventRegistrationCreateSerializer
        elif self.action == 'retrieve':
            return EventRegistrationGetSerializer
        elif self.action == 'update' or self.action == 'partial_update':
            return EventRegistrationPatchSerializer

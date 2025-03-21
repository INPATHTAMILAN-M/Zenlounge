from rest_framework import viewsets, permissions, filters
from ..models import EventLog
from ..serializers.event_log_serializer import EventLogGetSerializer, EventLogCreateSerializer, EventLogPatchSerializer, EventLogListSerializer
from ..filters import EventLogFilter

class EventLogViewSet(viewsets.ModelViewSet):
    queryset = EventLog.objects.all()
    serializer_class = EventLogListSerializer   
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'post','patch', 'delete']
    filterset_class = EventLogFilter

    def get_serializer_class(self):
        if self.action == 'list':
            return EventLogListSerializer
        elif self.action == 'create':
            return EventLogCreateSerializer
        elif self.action == 'retrieve':
            return EventLogGetSerializer
        elif self.action == 'update' or self.action == 'partial_update':
            return EventLogPatchSerializer

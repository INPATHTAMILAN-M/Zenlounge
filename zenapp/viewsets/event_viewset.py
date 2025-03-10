from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend
from ..filters.event_filters import EventFilter
from ..models import Event
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status
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
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.action == 'create':
            return EventCreateSerializer
        elif self.action == 'retrieve':
            return EventGetSerializer
        elif self.action == 'update' or self.action == 'partial_update':
            return EventPatchSerializer
        return EventListSerializer
    
    def get_permissions(self):
        if self.action == 'list':
            return []
        return super().get_permissions()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def list(self, request, *args, **kwargs):
        page_param = request.query_params.get('pagitation', None)
        if page_param == 'false':
            self.pagination_class = None
        else:
            self.pagination_class = PageNumberPagination
        return super().list(request, *args, **kwargs)
from rest_framework import viewsets
from ..serializers import GroupSerializer, GroupCreateSerializer, GroupUpdateSerializer, GroupListSerializer
from django.contrib.auth.models import Group


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all().exclude(id=2)
    serializer_class = GroupSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return GroupCreateSerializer
        elif self.action == 'update':
            return GroupUpdateSerializer
        elif self.action == 'list':
            return GroupListSerializer
        return super().get_serializer_class()
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from zenapp.models import ZoomMeetingAttendance
from ..serializers.zoom_meeting_attendance_serializer import ZoomMeetingAttendanceGetSerializer, ZoomMeetingAttendanceCreateSerializer, ZoomMeetingAttendancePatchSerializer, ZoomMeetingAttendanceListSerializer

class ZoomMeetingAttendanceViewSet(viewsets.ModelViewSet):
    queryset = ZoomMeetingAttendance.objects.all()
    serializer_class = ZoomMeetingAttendanceListSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post','patch', 'delete']

    def get_serializer_class(self):
        if self.action == 'list':
            return ZoomMeetingAttendanceListSerializer
        elif self.action == 'create':
            return ZoomMeetingAttendanceCreateSerializer
        elif self.action == 'retrieve':
            return ZoomMeetingAttendanceGetSerializer
        elif self.action == 'update' or self.action == 'partial_update':
            return ZoomMeetingAttendancePatchSerializer

from django_filters import rest_framework as filters
from zenapp.models import ZoomMeetingAttendance

class ZoomMeetingAttendanceFilter(filters.FilterSet):
    class Meta:
        model = ZoomMeetingAttendance
        fields = '__all__'

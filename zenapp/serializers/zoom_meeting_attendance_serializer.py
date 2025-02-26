from rest_framework import serializers
from zenapp.models import ZoomMeetingAttendance

class ZoomMeetingAttendanceGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = ZoomMeetingAttendance
        fields = '__all__'

class ZoomMeetingAttendanceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ZoomMeetingAttendance
        fields = '__all__'

class ZoomMeetingAttendancePatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = ZoomMeetingAttendance
        fields = '__all__'

class ZoomMeetingAttendanceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ZoomMeetingAttendance
        fields = '__all__'

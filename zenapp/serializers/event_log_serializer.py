from rest_framework import serializers
from zenapp.models import EventLog

class EventLogGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventLog
        fields = '__all__'

class EventLogCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventLog
        fields = '__all__'

class EventLogPatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventLog
        fields = '__all__'

class EventLogListSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventLog
        fields = '__all__'

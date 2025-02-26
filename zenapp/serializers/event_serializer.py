from rest_framework import serializers
from zenapp.models import Event

class EventListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

class EventGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

class EventCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

class EventPatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'
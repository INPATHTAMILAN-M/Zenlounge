from rest_framework import serializers
from authapp.models import CustomUser
from zenapp.models import Event, EventRegistration
from zenapp.serializers.event_serializer import CategorySerializer
import random
import string


class EventRegistrationCreateSerializer(serializers.ModelSerializer):
    event = serializers.ListField(child=serializers.IntegerField(), write_only=True)
    user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), write_only=True)

    class Meta:
        model = EventRegistration
        fields = '__all__'
            
    def validate_user(self, value):
        if value.groups.filter(name__iexact='admin').exists():
            raise serializers.ValidationError("Admins cannot register for events.")
        return value
    

    def create(self, validated_data):
        event_ids = validated_data.pop('event')
        user = validated_data.pop('user')

        registrations = []
        for event_id in event_ids:
            if EventRegistration.objects.filter(event_id=event_id, user=user).exists():
                raise serializers.ValidationError(f"Already registered for event ID {event_id}.")

            registration = EventRegistration.objects.create(
                registration_id=self.generate_registration_id(),
                event=Event.objects.get(id=event_id),
                user=user,
                **validated_data
            )
            registrations.append(registration)

        return registrations
    
class EventRegistrationPatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventRegistration
        fields = '__all__'

class EventListSerializer(serializers.ModelSerializer):
    lounge_type = CategorySerializer(read_only=True)
    class Meta:
        model = Event
        fields = '__all__'
class CustomUserListSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'username','profile_picture','phone_number','date_of_birth' ]
        
class EventRegistrationListSerializer(serializers.ModelSerializer):
    event=EventListSerializer()
    user=CustomUserListSerializer()
    class Meta:
        model = EventRegistration
        fields = '__all__'

class EventRegistrationGetSerializer(serializers.ModelSerializer):
    event=EventListSerializer()
    user=CustomUserListSerializer()
    class Meta:
        model = EventRegistration
        fields = '__all__'
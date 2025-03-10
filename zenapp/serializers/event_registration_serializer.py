from rest_framework import serializers
from authapp.models import CustomUser
from zenapp.models import Event, EventRegistration
from zenapp.serializers.event_serializer import CategorySerializer
import random
import string


class EventRegistrationCreateSerializer(serializers.ModelSerializer):
    event = serializers.ListField(
        child=serializers.IntegerField(), write_only=True
    )
    user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), write_only=True)
    class Meta:
        model = EventRegistration
        fields = '__all__'

    def generate_registration_id(self):
        """Generate a unique registration ID in the format 'order-XXXX'."""
        while True:
            # Create a random string of digits for the order number
            random_number = ''.join(random.choices(string.digits, k=5))
            registration_id = f"#{random_number}"
            
            # Ensure the generated ID is unique
            if not EventRegistration.objects.filter(registration_id=registration_id).exists():
                return registration_id

    def create(self, validated_data):
        event_ids = validated_data.pop('event')
        user = validated_data.pop('user')
        registrations = []

        for event_id in event_ids:
            # Check for existing registration for the same event and user
            if EventRegistration.objects.filter(event_id=event_id, user=user).exists():
                event = Event.objects.get(id=event_id)
                raise serializers.ValidationError(f"Registration for event {event.title} and user {user.username} already exists.")  # Skip creating a new registration if it already exists

            registration_id = self.generate_registration_id()
            event = Event.objects.get(id=event_id)
            registration_data = {
                'registration_id': registration_id,
                'event': event,
                'user': user,
                **validated_data
            }
            registration = EventRegistration.objects.create(**registration_data)
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
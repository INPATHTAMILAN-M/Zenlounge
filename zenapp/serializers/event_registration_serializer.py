from rest_framework import serializers
from authapp.models import CustomUser
from zenapp.models import Event, EventRegistration
from zenapp.serializers.event_serializer import CategorySerializer
from authapp.utils.email_sender import send_email  
from django.db import transaction

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

        events = Event.objects.filter(id__in=event_ids)  # Fetch all events at once

        if not events.exists():  # Ensure events list is not empty
            raise serializers.ValidationError("No valid events found for registration.")

        registrations = []

        with transaction.atomic():  # Ensures all or nothing
            for event in events:
                if EventRegistration.objects.filter(event=event, user=user).exists():
                    raise serializers.ValidationError(
                        f"{user.username} is already registered for the event: {event.title}. "
                        "Visit profile to see more details."
                    )

                registration = EventRegistration.objects.create(event=event, user=user, **validated_data)
                registrations.append(registration)

                context = {
                    "user_name": user.email,
                    "event_title": event.title,
                    "event_start_date": event.start_date,
                    "event_end_date": event.end_date,
                    "event_start_time": event.start_time,
                    "event_end_time": event.end_time,
                    "event_location": "Online",
                    "registration_id": registration.registration_id,
                    "registration_status": registration.registration_status,
                    "event_link": event.session_link,
                }
                send_email(subject="Event Registration Successful", to_email=user.email, template_name="event-registration.html", context=context)

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
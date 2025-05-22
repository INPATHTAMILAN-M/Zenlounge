from rest_framework import serializers
from authapp.models import CustomUser
from zenapp.models import Event, EventRegistration
from zenapp.serializers.event_serializer import CategorySerializer
from authapp.utils.email_sender import send_email  
from django.db import transaction


class EventRegistrationSerializer(serializers.ModelSerializer):
    event = serializers.StringRelatedField()  # Example: Use the event's `__str__` representation
    user = serializers.StringRelatedField()
    class Meta:
        model = EventRegistration
        fields = ['id', 'event', 'user', 'registration_status', 'registration_date']


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

        events = Event.objects.filter(id__in=event_ids)
        if not events.exists():
            raise serializers.ValidationError("No valid events found for registration.")

        registrations = []
        
        for event in events:
            if EventRegistration.objects.filter(event=event, user=user).exists():
                raise serializers.ValidationError(f"Already registered for {event.title}.")

            # Create the registration instance
            registration = EventRegistration.objects.create(event=event, user=user, **validated_data)
            registration.refresh_from_db()  # Ensure auto-generated fields are populated

            # Debugging: Print the registration_id to verify it is being set
            print(f"Created registration with ID: {registration.registration_id}")

            # Send email notification
            send_email(
                subject="Event Registration Successful",
                to_email=user.email,
                template_name="event-registration.html",
                context={
                    "user_name": user.email,
                    "event_title": event.title,
                    "event_start_date": event.start_date,
                    "event_end_date": event.end_date,
                    "event_start_time": event.start_time,
                    "event_end_time": event.end_time,
                    "event_location": "Online",
                    "registration_id": registration.registration_id,
                    "registration_status": registration.registration_status,
                    "event_link": "https://filez.zenwellnesslounge.com/view-order?id={}".format(event.id),
                }
            )
            registrations.append(registration)

        # Serialize and return the registrations
        serialized_data = EventRegistrationSerializer(registrations, many=True).data
        print(f"Serialized Data: {serialized_data}")  # Debugging: Check the serialized output
        return serialized_data
    
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
        fields = ['id', 'email', 'username','first_name','last_name','profile_picture','phone_number','date_of_birth' ]
        
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
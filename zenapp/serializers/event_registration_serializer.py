from rest_framework import serializers
from authapp.models import CustomUser
from zenapp.models import Event, EventRegistration
from zenapp.serializers.event_serializer import CategorySerializer
import random
import string
from authapp.utils.email_sender import send_email  

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

    def send_registration_email(self, user):
        """Send Registration Confirmation Email"""
        profile = CustomUser.objects.get(id=user.id)
        context = {
            "name": user.username,
            "emailaddress": user.email,
            "department": profile.department if profile.department else None,
            "yearofentry": profile.year_of_entry if profile.year_of_entry else None,
            # "interestedtopics": profile.interested_topics if profile.interested_topics else None,
            # "university": profile.university if profile.university else None
        }
        template = "student-registration.html" if user.groups.filter(name__iexact="Student").exists() else "alumni-registration.html"
        send_email(subject="Registration Successful", to_email=user.email, template_name=template, context=context)

    def create(self, validated_data):
        event_ids = validated_data.pop('event')
        user = validated_data.pop('user')

        registrations = []
        for event_id in event_ids:
            if EventRegistration.objects.filter(event_id=event_id, user=user).exists():
                event = Event.objects.get(id=event_id)
                raise serializers.ValidationError(f"{user.username} is already registered for the event: {event.title}.")

            registration = EventRegistration.objects.create(
                event=Event.objects.get(id=event_id),
                user=user,
                **validated_data
            )
            
            registrations.append(registration)
            self.send_registration_email(user)

        return registration
    
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
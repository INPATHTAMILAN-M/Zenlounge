from rest_framework import serializers
from authapp.models import CustomUser
from django.contrib.auth.models import Group
from ..models import Country, IntrestedTopic, University
from zenapp.models import EventRegistration
from authapp.utils.email_sender import send_email
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
import random
import string

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'name', 'code']

class UniversitySerializer(serializers.ModelSerializer):
    class Meta:
        model = University
        fields = '__all__'
        
class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']
class EveventRegistrationSerializer(serializers.ModelSerializer):
    event_title = serializers.SerializerMethodField()

    class Meta:
        model = EventRegistration
        fields = '__all__'

    def get_event_title(self, obj):
        return obj.event.title

class CustomUserCreateSerializer(serializers.ModelSerializer):
    groups = serializers.PrimaryKeyRelatedField(
        queryset=Group.objects.all(), many=True, required=False
    )


    class Meta:
        model = CustomUser
        fields = [
            'email', 'username', 'phone_number', 'address', 'date_of_birth',
            'university', 'intrested_topics', 'year_of_entry', 'profile_picture',
            'groups','department'
        ]

    def create(self, validated_data):
        groups = validated_data.pop('groups', None) or []

        password = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        validated_data['password'] = password

        user = CustomUser.objects.create(**validated_data)
        user.set_password(password)  # Set the generated password
        user.save()

        if groups:
            user.groups.set(groups)

        is_alumni = any(group.name == 'Alumni' for group in user.groups.all())

        if not is_alumni:
            reset_url = f"{settings.FRONTEND_URL}/login/"

            send_email(
                subject="Your Account Created",
                to_email=user.email,
                template_name='welcome_email.html',
                context={
                    "username": user.username,
                    "email": user.email,
                    "password": password,
                    "url": reset_url
                },
            )
        return user


class CustomUserUpdateSerializer(serializers.ModelSerializer):
    groups = serializers.PrimaryKeyRelatedField(
        queryset=Group.objects.all(), many=True, required=False
    )


    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'username', 'phone_number', 'address', 'date_of_birth', 
                  'university', 'intrested_topics', 'year_of_entry', 'profile_picture',
                  'groups','department']

    def update(self, instance, validated_data):
        groups = validated_data.pop('groups', instance.groups.all())
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        instance.groups.set(groups)  # Assign groups

        
        return instance

class CustomUserListSerializer(serializers.ModelSerializer):
    groups = serializers.StringRelatedField(many=True)
    event_registrations_count = serializers.SerializerMethodField()
    university = UniversitySerializer()
    country = CountrySerializer()
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'username', 'phone_number', 'address', 'date_of_birth', 
                  'university', 'intrested_topics', 'year_of_entry', 'profile_picture', 'department',
                  'groups', 'event_registrations_count','date_joined', 'country','work','year_of_graduation','is_open_to_be_mentor']

    def get_event_registrations_count(self, obj):
        return obj.event_registrations.count()  # Assuming event_registrations is a related name or field on CustomUser

class CustomUserDetailSerializer(serializers.ModelSerializer):

    event_registrations = EveventRegistrationSerializer(many=True, read_only=True)
    university = UniversitySerializer()
    country = CountrySerializer()
    group = serializers.SerializerMethodField() 
    
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'username', 'phone_number', 'address', 'date_of_birth','department',
                  'university', 'intrested_topics', 'year_of_entry', 'profile_picture',
                  'groups', 'event_registrations', 'date_joined', 'country', 'group','work','year_of_graduation','is_open_to_be_mentor']

    def get_group(self, obj):
        group = obj.groups.first() 
        if group:
            return {'id': group.id, 'name': group.name}
        return None 
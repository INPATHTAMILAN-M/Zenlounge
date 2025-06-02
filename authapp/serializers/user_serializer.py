from rest_framework import serializers
from authapp.models import CustomUser
from django.contrib.auth.models import Group
from ..models import Country, IntrestedTopic, University
from zenapp.models import EventRegistration
from authapp.utils.email_sender import send_email
from django.conf import settings
import random
import string
import json


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
    intrested_topics = serializers.PrimaryKeyRelatedField(
        queryset=IntrestedTopic.objects.all(), many=True, required=False
    )

    class Meta:
        model = CustomUser
        fields = [
            'email', 'username', 'phone_number', 'address', 'date_of_birth', "lable",
            'university', 'intrested_topics', 'year_of_entry', 'profile_picture', 'country',
            'first_name', 'last_name', 'groups', 'department', 'work', 'year_of_graduation',
            'is_open_to_be_mentor'
        ]

    def create(self, validated_data):
        groups = validated_data.pop('groups', [])
        intrested_topics = validated_data.pop('intrested_topics', [])

        password = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        user = CustomUser.objects.create(**validated_data)
        user.set_password(password)
        user.save()

        if groups:
            user.groups.set(groups)
        if intrested_topics:
            user.intrested_topics.set(intrested_topics)

        is_alumni = user.groups.filter(name='Alumni').exists()

        if not is_alumni:
            reset_url = f"{settings.FRONTEND_URL}/login/"
            send_email(
                subject="Your Account Created",
                to_email=user.email,
                template_name='welcome_email.html',
                context={
                    "username": f"{user.first_name} {user.last_name}",
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
    intrested_topics = serializers.PrimaryKeyRelatedField(
        queryset=IntrestedTopic.objects.all(), many=True, required=False
    )

    class Meta:
        model = CustomUser
        fields = [
            'id', 'email', 'username', 'phone_number', 'address', 'date_of_birth', 'first_name', 'last_name', "lable",
            'university', 'intrested_topics', 'year_of_entry', 'profile_picture', 'country',
            'groups', 'department', 'work', 'year_of_graduation', 'is_open_to_be_mentor'
        ]

    def update(self, instance, validated_data):
        groups = validated_data.pop('groups', None)
        intrested_topics = validated_data.pop('intrested_topics', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        if groups is not None:
            instance.groups.set(groups)
        if intrested_topics is not None:
            instance.intrested_topics.set(intrested_topics)

        return instance

from rest_framework import serializers
from authapp.models import IntrestedTopic

class IntrestedTopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntrestedTopic
        fields = '__all__'


class CustomUserListSerializer(serializers.ModelSerializer):
    groups = serializers.StringRelatedField(many=True)
    event_registrations_count = serializers.SerializerMethodField()
    university = UniversitySerializer()
    country = CountrySerializer()
    intrested_topics = IntrestedTopicSerializer(many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = [
            'id', 'email', 'username', 'phone_number', 'address', 'date_of_birth',"lable",
            'first_name','last_name','university', 'intrested_topics', 'year_of_entry', 
            'profile_picture','department', 'groups', 'event_registrations_count', 'date_joined',
            'country', 'work', 'year_of_graduation', 'is_open_to_be_mentor'
        ]

    def get_event_registrations_count(self, obj):
        return obj.event_registrations.count()
    


    # def to_representation(self, instance):
    #     data = super().to_representation(instance)
    #     try:
    #         data['intrested_topics'] = json.loads(data['intrested_topics']) if data['intrested_topics'] else []
    #     except (TypeError, json.JSONDecodeError):
    #         data['intrested_topics'] = []
    #     return data

class CustomUserDetailSerializer(serializers.ModelSerializer):
    event_registrations = EveventRegistrationSerializer(many=True, read_only=True)
    university = UniversitySerializer()
    country = CountrySerializer()
    group = serializers.SerializerMethodField() 

    class Meta:
        model = CustomUser
        fields = [
            'id', 'email', 'username', 'phone_number', 'address', 'date_of_birth', 'department',
            'university', 'intrested_topics', 'year_of_entry', 'profile_picture','first_name','last_name',
            'groups', 'event_registrations', 'date_joined', 'country', 'group',
            'work', 'year_of_graduation', 'is_open_to_be_mentor'
        ]

    def get_group(self, obj):
        group = obj.groups.first()
        if group:
            return {'id': group.id, 'name': group.name}
        return None

    def to_representation(self, instance):
        data = super().to_representation(instance)
        try:
            data['intrested_topics'] = json.loads(data['intrested_topics']) if data['intrested_topics'] else []
        except (TypeError, json.JSONDecodeError):
            data['intrested_topics'] = []
        return data
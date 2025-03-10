from rest_framework import serializers
from authapp.models import CustomUser
from django.contrib.auth.models import Group
from ..models import IntrestedTopic
from zenapp.models import EventRegistration
from authapp.utils.email_sender import send_email

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
            'email', 'username', 'phone_number', 'address', 'date_of_birth',
            'university', 'intrested_topics', 'year_of_entry', 'profile_picture',
            'groups'
        ]

    def create(self, validated_data):
        groups = validated_data.pop('groups', [])
        intrested_topics = validated_data.pop('intrested_topics', [])
        user = CustomUser.objects.create(**validated_data)
        user.groups.set(groups)  # Assign groups
        user.intrested_topics.set(intrested_topics)  # Assign interested topics
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
        fields = ['id', 'email', 'username', 'phone_number', 'address', 'date_of_birth', 
                  'university', 'intrested_topics', 'year_of_entry', 'profile_picture', 
                  'groups']

    def update(self, instance, validated_data):
        groups = validated_data.pop('groups', instance.groups.all())
        intrested_topics = validated_data.pop('intrested_topics', instance.intrested_topics.all())
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        instance.groups.set(groups)  # Assign groups
        instance.intrested_topics.set(intrested_topics)  # Assign interested topics
        
        return instance

class CustomUserListSerializer(serializers.ModelSerializer):
    groups = serializers.StringRelatedField(many=True)
    event_registrations_count = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'username', 'phone_number', 'address', 'date_of_birth', 
                  'university', 'intrested_topics', 'year_of_entry', 'profile_picture', 
                  'groups', 'event_registrations_count','date_joined']

    def get_event_registrations_count(self, obj):
        return obj.event_registrations.count()  # Assuming event_registrations is a related name or field on CustomUser

class CustomUserDetailSerializer(serializers.ModelSerializer):
    group_name = serializers.SerializerMethodField()
    event_registrations = EveventRegistrationSerializer(many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'username', 'phone_number', 'address', 'date_of_birth',
                  'university', 'intrested_topics', 'year_of_entry', 'profile_picture',
                  'groups', 'event_registrations', 'date_joined', 'group_name']

    def get_group_name(self, obj):
        group_names = [group.name for group in obj.groups.all()]
        return ', '.join(group_names)
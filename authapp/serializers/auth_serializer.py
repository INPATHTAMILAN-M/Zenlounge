import json
import string

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group
from django.utils.crypto import get_random_string

from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from authapp.models import CustomUser
from authapp.utils.email_sender import send_email

class UserSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False, min_length=6, 
                                     validators=[validate_password])
    is_alumni = serializers.BooleanField(default=False)
    intrested_topics = serializers.JSONField(required=False)
    class Meta:
        model = CustomUser
        fields = [
            "username",
            "email",
            "password",
            "phone_number",
            "address",
            "date_of_birth",
            "university",
            "department",
            "intrested_topics",  # keep typo to match model
            "year_of_entry",
            "work",
            "profile_picture",
            "year_of_graduation",
            "country",
            "is_open_to_be_mentor",
            "is_alumni"
        ]

    def send_registration_email(self, user):
        profile = CustomUser.objects.get(id=user.id)
        context = {
            "role": "Alumni" if user.groups.filter(name__iexact="Alumni").exists() else "Student",
            "name": user.username,
            "yeargraduated": profile.year_of_graduation or ' ',
            "department": profile.department or ' ',
            "work": profile.work or ' ',
            "country": profile.country or ' ',
            "address": profile.address or ' ',
            "yearofentry": profile.year_of_entry or ' ',
            "emailaddress": user.email,
            "phonenumber": profile.phone_number or ' ',
            "mentor": "Yes" if profile.is_open_to_be_mentor else "No",
            "interestedtopics": ', '.join(json.loads(profile.intrested_topics)) if profile.intrested_topics else ' ',
            "university": profile.university.name if profile.university else ' ',
        }
        template = "student-registration.html" if user.groups.filter(name__iexact="Student").exists() else "alumni-registration.html"
        send_email(subject="Registration Successful", to_email=user.email, template_name=template, context=context)

    def validate_intrested_topics(self, value):
        """
        Accept list or comma-separated string, return as JSON string.
        """
        print (f"Validating interested topics: {value}")
        if isinstance(value, list):
            return json.dumps(value)
        elif isinstance(value, str):
            return json.dumps([t.strip() for t in value.split(",") if t.strip()])
        return json.dumps([])

    def create(self, validated_data):
        alumni = validated_data.pop("is_alumni", None)

        # if not validated_data.get('password'):
        #     validated_data['password'] = get_random_string()
        user = CustomUser.objects.create(**validated_data)

        group_name = "Alumni" if alumni else "Student"
        group, _ = Group.objects.get_or_create(name=group_name)
        user.groups.add(group)

        self.send_registration_email(user)
        return user


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

class PasswordConfirmSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True, min_length=6)
    confirm_password = serializers.CharField(write_only=True, min_length=6)

    def validate(self, data):
        if data["new_password"] != data["confirm_password"]:
            raise serializers.ValidationError("Passwords do not match.")
        return data



from rest_framework import serializers
from django.contrib.auth import password_validation


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)
    confirm_password = serializers.CharField(required=True, write_only=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect.")
        return value

    def validate(self, data):
        if data["new_password"] != data["confirm_password"]:
            raise serializers.ValidationError({"confirm_password": "New password and confirm password do not match."})
        
        # Validate password complexity
        password_validation.validate_password(data["new_password"], self.context['request'].user)
        
        return data


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
    password = serializers.CharField(
        write_only=True,
        required=False,
        min_length=8,
        validators=[validate_password]
    )
    is_alumni = serializers.BooleanField(default=False)
    intrested_topics = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=CustomUser._meta.get_field('intrested_topics').related_model.objects.all(),
        required=False
    )

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
            "lable",
            "year_of_entry",
            "first_name",
            "last_name",
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
            "name": user.first_name + " " + user.last_name,
            "yeargraduated": profile.year_of_graduation or ' ',
            "department": profile.department or ' ',
            "work": profile.work or ' ',
            "country": profile.country or ' ',
            "address": profile.address or ' ',
            "yearofentry": profile.year_of_entry or ' ',
            "emailaddress": user.email,
            "phonenumber": profile.phone_number or ' ',
            "mentor": "Yes" if profile.is_open_to_be_mentor else "No",
            "interestedtopics": ', '.join([str(t) for t in profile.intrested_topics.all()]) if profile.intrested_topics.exists() else ' ',
            "university": profile.university.name if profile.university else ' ',
        }
        template = "student-registration.html" if user.groups.filter(name__iexact="Student").exists() else "alumni-registration.html"
        subject = "Welcome! Your Student Registration is Confirmed – Next Steps Inside" if user.groups.filter(name__iexact="Student").exists() else "Welcome to the Alumni Community – Next Steps"
        send_email(subject=subject, to_email=user.email, template_name=template, context=context)

    def create(self, validated_data):
        alumni = validated_data.pop("is_alumni", None)
        intrested_topics = validated_data.pop("intrested_topics", [])

        user = CustomUser.objects.create(**validated_data)

        if intrested_topics:
            user.intrested_topics.set(intrested_topics)

        group_name = "Alumni" if alumni else "Student"
        group, _ = Group.objects.get_or_create(name=group_name)
        user.groups.add(group)

        self.send_registration_email(user)
        return user


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            user = CustomUser.objects.get(email=value)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("User with this email does not exist.")
        return value

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

    def validate_new_password(self, value):
        # Additional password validation
        password_validation.validate_password(value, self.context['request'].user)
        return value


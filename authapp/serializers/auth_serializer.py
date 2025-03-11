from rest_framework import serializers
from authapp.models import CustomUser
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group

class UserSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=6, validators=[validate_password])
    is_alumni = serializers.BooleanField(default=False)

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
            "intrested_topics",
            "year_of_entry",
            "work",
            "profile_picture",
            "year_of_graduation",
            "country",
            "is_open_to_be_mentor",
            "is_alumni"  # Added is_alumni to the fields list
        ]

    def create(self, validated_data):
        # Hash the password before saving the user
        validated_data["password"] = make_password(validated_data["password"])
        alumni = validated_data.pop("is_alumni", None)  # Remove is_alumni from validated_data
        user = CustomUser.objects.create(**validated_data)

        # Assign user to a default group (Students or Professors)
        if alumni:
            group, _ = Group.objects.get_or_create(name="Alumni")
        else:
            group, _ = Group.objects.get_or_create(name="Student")
            
        user.groups.add(group)

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




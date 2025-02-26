from rest_framework import serializers
from authapp.models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'phone_number', 'address', 'date_of_birth', 'university', 'intrested_topics', 'year_of_entry', 'profile_picture']

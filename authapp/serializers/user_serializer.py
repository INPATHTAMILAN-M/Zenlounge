from rest_framework import serializers
from authapp.models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    groups = serializers.StringRelatedField(many=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'email','username', 'phone_number', 'address', 'date_of_birth', 
                  'university', 'intrested_topics', 'year_of_entry', 'profile_picture',
                  'groups']
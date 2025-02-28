from rest_framework import serializers
from authapp.models import CustomUser

class CustomUserCreateSerializer(serializers.ModelSerializer):
    groups = serializers.StringRelatedField(many=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'phone_number', 'address', 'date_of_birth', 
                  'university', 'intrested_topics', 'year_of_entry', 'profile_picture', 
                  'groups']

    def create(self, validated_data):
        user = CustomUser.objects.create(**validated_data)
        user.save()
        user.groups.set(validated_data['groups'])
        return user

class CustomUserUpdateSerializer(serializers.ModelSerializer):
    groups = serializers.StringRelatedField(many=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'username', 'phone_number', 'address', 'date_of_birth', 
                  'university', 'intrested_topics', 'year_of_entry', 'profile_picture', 
                  'groups']

class CustomUserListSerializer(serializers.ModelSerializer):
    groups = serializers.StringRelatedField(many=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'username', 'phone_number', 'address', 'date_of_birth', 
                  'university', 'intrested_topics', 'year_of_entry', 'profile_picture', 
                  'groups']

class CustomUserDetailSerializer(serializers.ModelSerializer):
    groups = serializers.StringRelatedField(many=True)
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'username', 'phone_number', 'address', 'date_of_birth',
                  'university', 'intrested_topics', 'year_of_entry', 'profile_picture',
                  'groups']

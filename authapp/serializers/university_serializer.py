from rest_framework import serializers
from authapp.models import University


class UniversitySerializer(serializers.ModelSerializer):
    class Meta:
        model = University
        fields = '__all__'
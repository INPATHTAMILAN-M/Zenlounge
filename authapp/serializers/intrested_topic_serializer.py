from rest_framework import serializers
from authapp.models import IntrestedTopic

class IntrestedTopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntrestedTopic
        fields = '__all__'
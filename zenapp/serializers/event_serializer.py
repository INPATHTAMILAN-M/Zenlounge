from rest_framework import serializers
from zenapp.models import Event, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class EventListSerializer(serializers.ModelSerializer):
    lounge_type = CategorySerializer(read_only=True)
    class Meta:
        model = Event
        fields = '__all__'

class EventGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

class EventCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

class EventPatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'
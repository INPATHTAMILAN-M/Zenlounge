from rest_framework import serializers
from zenapp.models import Event, Category, EventRegistration


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
    lounge_type = CategorySerializer(read_only=True)
    is_registered = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = '__all__'

    def get_is_registered(self, obj):
        request = self.context.get('request', None)
        if request and request.user.is_authenticated:
            return EventRegistration.objects.filter(event=obj, user=request.user).exists()
        return False

class EventCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

class EventPatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'
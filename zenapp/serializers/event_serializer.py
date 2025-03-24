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

    def validate(self, data):
        # Ensure end_time is not before start_time
        start_time = data.get('start_time', self.instance.start_time if self.instance else None)
        end_time = data.get('end_time', self.instance.end_time if self.instance else None)

        if start_time and end_time and end_time < start_time:
            raise serializers.ValidationError("End time cannot be before start time.")

        # Ensure start_time and end_time are not in the past during update
        if self.instance:  # Only check during updates
            if start_time and start_time < self.instance.start_time:
                raise serializers.ValidationError("Start time cannot be in the past.")
            if end_time and end_time < self.instance.end_time:
                raise serializers.ValidationError("End time cannot be in the past.")

        return data
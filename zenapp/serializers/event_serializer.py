from rest_framework import serializers
from zenapp.models import Event, Category, EventRegistration
from django.utils.timezone import now


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

    def validate_start_date(self, value):
        """Ensure start_date is not in the past."""
        if value < now().date():
            raise serializers.ValidationError("Start date cannot be in the past.")
        return value

    def validate_end_date(self, value):
        """Ensure end_date is not before start_date."""
        if 'start_date' in self.initial_data:
            start_date = self.initial_data['start_date']
            if value < start_date:
                raise serializers.ValidationError("End date cannot be before start date.")
        return value

    def validate(self, data):
        """Ensure time and date constraints are met."""
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        start_time = data.get('start_time')
        end_time = data.get('end_time')

        current_date = now().date()
        current_time = now().time()

        # Validate time consistency
        if start_date and end_date and end_date < start_date:
            raise serializers.ValidationError({"end_date": "End date cannot be before start date."})

        if start_date and start_date == current_date and start_time and start_time < current_time:
            raise serializers.ValidationError({"start_time": "Start time cannot be in the past."})

        if start_date and end_date and start_date == end_date and start_time and end_time and end_time < start_time:
            raise serializers.ValidationError({"end_time": "End time cannot be before start time on the same day."})

        return data

class EventPatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

    def validate(self, data):
        """Ensure time and date constraints are met (even for partial updates)."""
        start_date = data.get('start_date', getattr(self.instance, 'start_date', None))
        end_date = data.get('end_date', getattr(self.instance, 'end_date', None))
        start_time = data.get('start_time', getattr(self.instance, 'start_time', None))
        end_time = data.get('end_time', getattr(self.instance, 'end_time', None))

        current_date = now().date()
        current_time = now().time()

        # Validate time consistency
        if start_date and end_date and end_date < start_date:
            raise serializers.ValidationError({"end_date": "End date cannot be before start date."})

        if start_date and start_date == current_date and start_time and start_time < current_time:
            raise serializers.ValidationError({"start_time": "Start time cannot be in the past."})

        if start_date and end_date and start_date == end_date and start_time and end_time and end_time < start_time:
            raise serializers.ValidationError({"end_time": "End time cannot be before start time on the same day."})

        return data

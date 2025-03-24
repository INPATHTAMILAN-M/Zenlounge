from rest_framework import serializers
from zenapp.models import Event, Category, EventRegistration
from django.utils.timezone import now
from datetime import datetime


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
        if isinstance(value, str):  # Convert string to date if needed
            value = datetime.strptime(value, "%Y-%m-%d").date()

        if value < now().date():
            raise serializers.ValidationError("Start date cannot be in the past.")
        return value

    def validate_end_date(self, value):
        """Ensure end_date is not before start_date."""
        if isinstance(value, str):  # Convert string to date if needed
            value = datetime.strptime(value, "%Y-%m-%d").date()

        start_date = self.initial_data.get("start_date")
        if start_date:
            if isinstance(start_date, str):
                start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
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

        # Convert strings to date/time objects
        if isinstance(start_date, str):
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        if isinstance(end_date, str):
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
        if isinstance(start_time, str):
            start_time = datetime.strptime(start_time, "%H:%M:%S").time()
        if isinstance(end_time, str):
            end_time = datetime.strptime(end_time, "%H:%M:%S").time()

        # Validate date logic
        if start_date and end_date and end_date < start_date:
            raise serializers.ValidationError({"end_date": "End date cannot be before start date."})

        # Ensure start time is not in the past if start date is today
        if start_date and start_date == current_date and start_time and start_time < current_time:
            raise serializers.ValidationError({"start_time": "Start time cannot be in the past."})

        # Ensure end_time is not before start_time on the same date
        if start_date and end_date and start_date == end_date and start_time and end_time and end_time < start_time:
            raise serializers.ValidationError({"end_time": "End time cannot be before start time on the same day."})

        return data

class EventPatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

    def validate(self, data):
        """Ensure date and time constraints are met even for partial updates."""
        start_date = data.get('start_date', getattr(self.instance, 'start_date', None))
        end_date = data.get('end_date', getattr(self.instance, 'end_date', None))
        start_time = data.get('start_time', getattr(self.instance, 'start_time', None))
        end_time = data.get('end_time', getattr(self.instance, 'end_time', None))

        current_date = now().date()
        current_time = now().time()

        # Ensure start_date is not in the past
        if start_date and start_date < current_date:
            raise serializers.ValidationError({"start_date": "Start date cannot be in the past."})

        # Ensure end_date is not in the past
        if end_date and end_date < current_date:
            raise serializers.ValidationError({"end_date": "End date cannot be in the past."})

        # Ensure end_date is not before start_date
        if start_date and end_date and end_date < start_date:
            raise serializers.ValidationError({"end_date": "End date cannot be before start date."})

        # Ensure start_time is not in the past if start_date is today
        if start_date == current_date and "start_time" in data and start_time and start_time < current_time:
            raise serializers.ValidationError({"start_time": "Start time cannot be in the past."})

        # Ensure end_time is not in the past if end_date is today
        if end_date == current_date and "end_time" in data and end_time and end_time < current_time:
            raise serializers.ValidationError({"end_time": "End time cannot be in the past."})

        # Ensure end_time is not before start_time on the same day
        if start_date and end_date and start_date == end_date and start_time and end_time:
            if "end_time" in data and end_time < start_time:
                raise serializers.ValidationError({"end_time": "End time cannot be before start time on the same day."})

        return data

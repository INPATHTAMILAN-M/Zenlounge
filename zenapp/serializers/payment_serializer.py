from rest_framework import serializers
from zenapp.models import Payment

class PaymentGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

class PaymentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

class PaymentPatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

class PaymentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

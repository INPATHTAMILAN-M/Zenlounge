from rest_framework import serializers
from zenapp.models import Payment


class PaymentGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

class PaymentCreateSerializer(serializers.ModelSerializer):
    currency = serializers.CharField(max_length=3, required=True)

    class Meta:
        model = Payment
        fields = ['registration', 'payment_gateway', 'currency']

class PaymentPatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

class PaymentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

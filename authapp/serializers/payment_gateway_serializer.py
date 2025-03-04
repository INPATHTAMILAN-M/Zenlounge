from rest_framework import serializers
from authapp.models import PaymentGateway

class PaymentGatewayRetriveSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentGateway
        fields = '__all__'

class PaymentGatewayCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentGateway
        fields = '__all__'

    def validate(self, data):
        if data.get('name') == 'razorpay':
            credentials = data.get('credentials', {})
            if 'public_key' not in credentials or 'secret_key' not in credentials:
                raise serializers.ValidationError("Razorpay credentials must include 'public_key' and 'secret_key'.")
        
        if data.get('name') == 'ccavenue':
            credentials = data.get('credentials', {})
            if 'merchant_code' not in credentials or 'access_code' not in credentials or 'working_key' not in credentials:
                raise serializers.ValidationError("CCAvenue credentials must include 'merchant_code', 'access_code', and 'working_key'.")
        
        return data

class PaymentGatewayUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentGateway
        fields = ['description', 'credentials']

    def validate(self, data):
        if self.instance and self.instance.name != data.get('name'):
            raise serializers.ValidationError("Changing the payment gateway name is not allowed.")
        
        if data.get('name') == 'razorpay':
            credentials = data.get('credentials', {})
            if 'public_key' not in credentials or 'secret_key' not in credentials:
                raise serializers.ValidationError("Razorpay credentials must include 'public_key' and 'secret_key'.")
        
        if data.get('name') == 'ccavenue':
            credentials = data.get('credentials', {})
            if 'merchant_code' not in credentials or 'access_code' not in credentials or 'working_key' not in credentials:
                raise serializers.ValidationError("CCAvenue credentials must include 'merchant_code', 'access_code', and 'working_key'.")
        
        return data

class PaymentGatewayListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentGateway
        fields = '__all__'

from rest_framework import serializers
from ..models import Payment  # Adjust according to your project structure

class PaymentVerificationSerializer(serializers.Serializer):
    payment_id = serializers.IntegerField(required=False)  

    # Razorpay Fields
    razorpay_payment_id = serializers.CharField(required=False)
    razorpay_order_id = serializers.CharField(required=False)
    razorpay_signature = serializers.CharField(required=False)
    
    # CCAvenue Fields
    ccavenue_order_id = serializers.CharField(required=False)
    ccavenue_tracking_id = serializers.CharField(required=False)
    ccavenue_status = serializers.CharField(required=False)
    ccavenue_checksum = serializers.CharField(required=False)

    def validate_payment_id(self, value):
        """Retrieve and return the Payment instance for verification."""
        payment = Payment.objects.filter(id=value).first()
        if not payment:
            raise serializers.ValidationError("Invalid payment ID.")
        return payment  # Returning instance instead of just ID

    def validate(self, data):
        """Ensure at least one gateway's fields are provided."""
        has_razorpay = all(data.get(f) for f in ["razorpay_payment_id", "razorpay_order_id", "razorpay_signature"])
        has_ccavenue = all(data.get(f) for f in ["ccavenue_order_id", "ccavenue_tracking_id", "ccavenue_status", "ccavenue_checksum"])

        if not has_razorpay and not has_ccavenue:
            raise serializers.ValidationError("Provide either Razorpay or CCAvenue payment details.")

        return data
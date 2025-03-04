import razorpay
import hashlib
import hmac
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from razorpay.errors import SignatureVerificationError
from .models import Payment
from .serializers import PaymentVerificationSerializer

class PaymentVerificationView(APIView):
    serializer_class = PaymentVerificationSerializer()

    def post(self, request, *args, **kwargs):
        serializer = PaymentVerificationSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        validated_data = serializer.validated_data
        payment_gateway = validated_data["payment_gateway"]
        public_key = payment_id.payment_gateway.credentials.get("public_key"),
        secret_key = payment_id.payment_gateway.credentials.get("secret_key")

        # ✅ RAZORPAY VERIFICATION
        if payment_gateway == "razorpay":
            payment_id = validated_data.get("razorpay_payment_id")
            order_id = validated_data.get("razorpay_order_id")
            signature = validated_data.get("razorpay_signature")

            if not all([payment_id, order_id, signature]):
                return Response({"error": "Missing required parameters for Razorpay"}, status=status.HTTP_400_BAD_REQUEST)

            client = razorpay.Client(auth=(public_key, secret_key))
            
            try:
                client.utility.verify_payment_signature({
                    "razorpay_order_id": order_id,
                    "razorpay_payment_id": payment_id,
                    "razorpay_signature": signature
                })
                
                Payment.objects.filter(order_id=order_id).update(status="completed")
                return Response({"message": "Razorpay Payment Verified Successfully"}, status=status.HTTP_200_OK)

            except SignatureVerificationError:
                Payment.objects.filter(order_id=order_id).update(status="failed")
                return Response({"error": "Razorpay Signature Verification Failed"}, status=status.HTTP_400_BAD_REQUEST)

        # ✅ CCAVENUE VERIFICATION
        elif payment_gateway == "ccavenue":
            order_id = validated_data.get("ccavenue_order_id")
            tracking_id = validated_data.get("ccavenue_tracking_id")
            status_text = validated_data.get("ccavenue_status")
            checksum = validated_data.get("ccavenue_checksum")

            if not all([order_id, tracking_id, status_text, checksum]):
                return Response({"error": "Missing required parameters for CCAvenue"}, status=status.HTTP_400_BAD_REQUEST)

            # Fetch the working key for checksum verification
            payment = Payment.objects.filter(order_id=order_id).first()
            if not payment:
                return Response({"error": "Payment record not found"}, status=status.HTTP_404_NOT_FOUND)
            
            working_key = payment.payment_gateway.working_key

            # Validate CCAvenue checksum
            generated_checksum = hmac.new(
                working_key.encode(), 
                f"{order_id}|{tracking_id}|{status_text}".encode(), 
                hashlib.sha256
            ).hexdigest()

            if generated_checksum.lower() != checksum.lower():
                return Response({"error": "CCAvenue Checksum Verification Failed"}, status=status.HTTP_400_BAD_REQUEST)

            # Update payment status
            Payment.objects.filter(order_id=order_id).update(status="completed")
            return Response({"message": "CCAvenue Payment Verified Successfully"}, status=status.HTTP_200_OK)
        
        Payment.objects.filter(order_id=order_id).update(status="failed")
        return Response({"error": "Invalid Payment Gateway"}, status=status.HTTP_400_BAD_REQUEST)
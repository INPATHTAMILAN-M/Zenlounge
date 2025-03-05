from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import razorpay
import hmac
import hashlib
from .models import Payment
from .serializers import PaymentVerificationSerializer
from authapp.utils.email_sender import send_email  # Assuming send_email is in utils.py

class PaymentVerificationView(APIView):
    serializer_class = PaymentVerificationSerializer()

    def post(self, request, *args, **kwargs):
        serializer = PaymentVerificationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        payment_gateway = validated_data.get("payment_gateway")

        if payment_gateway == "razorpay":
            return self.verify_razorpay(validated_data, request.user)
        elif payment_gateway == "ccavenue":
            return self.verify_ccavenue(validated_data)
        
        return Response({"error": "Invalid Payment Gateway"}, status=status.HTTP_400_BAD_REQUEST)

    def verify_razorpay(self, data, user):
        """Razorpay Payment Verification"""
        required_fields = ["razorpay_payment_id", "razorpay_order_id", "razorpay_signature"]
        if not all(data.get(field) for field in required_fields):
            return Response({"error": "Missing required Razorpay parameters"}, status=status.HTTP_400_BAD_REQUEST)

        payment_id, order_id, signature = data["razorpay_payment_id"], data["razorpay_order_id"], data["razorpay_signature"]
        payment = Payment.objects.filter(order_id=order_id).first()

        if not payment:
            return Response({"error": "Payment record not found"}, status=status.HTTP_404_NOT_FOUND)

        client = razorpay.Client(auth=(payment.payment_gateway.credentials["public_key"], payment.payment_gateway.credentials["secret_key"]))
        
        try:
            client.utility.verify_payment_signature({
                "razorpay_order_id": order_id,
                "razorpay_payment_id": payment_id,
                "razorpay_signature": signature
            })
            payment.status = "completed"
            payment.save()

            self.send_registration_email(user)
            return Response({"message": "Razorpay Payment Verified Successfully"}, status=status.HTTP_200_OK)

        except razorpay.errors.SignatureVerificationError:
            payment.status = "failed"
            payment.save()
            return Response({"error": "Razorpay Signature Verification Failed"}, status=status.HTTP_400_BAD_REQUEST)

    def verify_ccavenue(self, data):
        """CCAvenue Payment Verification"""
        required_fields = ["ccavenue_order_id", "ccavenue_tracking_id", "ccavenue_status", "ccavenue_checksum"]
        if not all(data.get(field) for field in required_fields):
            return Response({"error": "Missing required CCAvenue parameters"}, status=status.HTTP_400_BAD_REQUEST)

        order_id, tracking_id, status_text, checksum = data["ccavenue_order_id"], data["ccavenue_tracking_id"], data["ccavenue_status"], data["ccavenue_checksum"]
        payment = Payment.objects.filter(order_id=order_id).first()

        if not payment:
            return Response({"error": "Payment record not found"}, status=status.HTTP_404_NOT_FOUND)

        working_key = payment.payment_gateway.working_key
        generated_checksum = hmac.new(working_key.encode(), f"{order_id}|{tracking_id}|{status_text}".encode(), hashlib.sha256).hexdigest()

        if generated_checksum.lower() != checksum.lower():
            return Response({"error": "CCAvenue Checksum Verification Failed"}, status=status.HTTP_400_BAD_REQUEST)

        payment.status = "completed"
        payment.save()
        return Response({"message": "CCAvenue Payment Verified Successfully"}, status=status.HTTP_200_OK)

    def send_registration_email(self, user):
        """Send Registration Confirmation Email"""
        context = {
            "name": user.name,
            "emailaddress": user.email,
            "department": user.department,
            "yearofentry": user.year_of_entry,
            "interestedtopics": user.interested_topics,
            "university": user.university
        }
        template = "student-registration.html" if user.group.name == "Student" else "alumini-registration.html"
        send_email(subject="Registered Successful", to_email=user.email, template_name=template, context=context)
from rest_framework import viewsets, permissions, filters
from rest_framework.response import Response
from ..models import Payment
from common.payment.razorpay_client import RazorpayGateway
from common.payment.ccavenue_client import CCAvenueGateway
from ..serializers.payment_serializer import PaymentGetSerializer, PaymentCreateSerializer, PaymentPatchSerializer, PaymentListSerializer
from ..filters import PaymentFilter

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentListSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'post','patch', 'delete']
    filterset_class = PaymentFilter

    def get_serializer_class(self):
        if self.action == 'list':
            return PaymentListSerializer
        elif self.action == 'create':
            return PaymentCreateSerializer
        elif self.action == 'retrieve':
            return PaymentGetSerializer
        elif self.action == 'update' or self.action == 'partial_update':
            return PaymentPatchSerializer
        

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        gateway = validated_data["payment_gateway"]
        gateway_name = gateway.name.lower()
        credentials = gateway.get_credentials()
        registration = validated_data["registration"]
        user = self.request.user  # Use `self.request.user`

        # Get amount from event
        amount = registration.event.price

        # Save Payment object
        payment = serializer.save(user=user, amount=amount, status="pending")

        # Process payment
        if gateway_name == "razorpay":
            client = RazorpayGateway(
                credentials.get("public_key"),
                credentials.get("secret_key")
            )
            client.initialize_payment({
                "amount": amount,
                "currency": validated_data["currency"],
                "receipt": f"order_{payment.id}",
                "payment_capture": 1
            })
            response = client.process_payment()
            payment.save()  # Ensure payment is saved before returning
            return response

        elif gateway_name == "ccavenue":
            client = CCAvenueGateway(
                credentials.get("merchant_code"),
                credentials.get("access_code"),
                credentials.get("working_key")
            )
            response = client.initialize_payment({
                "amount": amount,
                "currency": validated_data["currency"],
                "merchant_param1": payment.id
            })
            client.process_payment()
            payment.save()
            return Response(response)  # Wrap response in Response

        raise serializers.ValidationError("Invalid payment gateway")
        

    

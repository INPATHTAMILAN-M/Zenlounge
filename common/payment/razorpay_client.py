import razorpay
from django.http import JsonResponse

from .payment_gateway import PaymentGateway

class RazorpayGateway(PaymentGateway):
    def __init__(self, api_key, api_secret):
        """
        Initialize Razorpay client with API key and secret.
        """
        self.client = razorpay.Client(auth=(api_key, api_secret))
        self.payment_data = None

    def initialize_payment(self, payment_data):
        """
        Initialize payment with the given data.
        """
        self.payment_data = payment_data

    def process_payment(self):
        """
        Create an order in Razorpay and return the order details.
        """
        if not self.payment_data:
            return JsonResponse({"error": "Payment data not initialized."}, status=400)
        
        # Prepare the order data
        order_data = {
            "amount": int(float(self.payment_data['amount']) * 100),  # Amount in paise
            "currency": self.payment_data['currency'],
            "receipt": self.payment_data.get('order_id', 'ORDER_RECEIPT'),
            "payment_capture": self.payment_data.get('payment_capture', 1)  # Auto-capture payment
        }
        
        try:
            # Create the order in Razorpay
            order_response = self.client.order.create(order_data)
            return JsonResponse(order_response, status=200)
        except razorpay.errors.BadRequestError as e:
            return JsonResponse({"error": f"Bad request error: {e}"}, status=400)
        except razorpay.errors.ServerError as e:
            return JsonResponse({"error": f"Server error: {e}"}, status=500)
        except Exception as e:
            return JsonResponse({"error": f"An unexpected error occurred: {e}"}, status=500)

    def handle_response(self, response_data):
        """
        Handle the payment response from Razorpay.
        """
        # Fetch payment details using the payment ID
        payment_id = response_data.get('razorpay_payment_id')
        if not payment_id:
            return JsonResponse({"error": "Invalid Razorpay response: Missing payment ID."}, status=400)
        
        try:
            payment_details = self.client.payment.fetch(payment_id)
            return JsonResponse(payment_details, status=200)
        except razorpay.errors.BadRequestError as e:
            return JsonResponse({"error": f"Bad request error: {e}"}, status=400)
        except razorpay.errors.ServerError as e:
            return JsonResponse({"error": f"Server error: {e}"}, status=500)
        except Exception as e:
            return JsonResponse({"error": f"An unexpected error occurred: {e}"}, status=500)

    def verify_payment_signature(self, response_data):
        """
        Verify the payment signature returned by Razorpay.
        """
        try:
            # Verify the signature using Razorpay's utility method
            self.client.utility.verify_payment_signature(response_data)
            return JsonResponse({"success": True}, status=200)
        except razorpay.errors.SignatureVerificationError:
            return JsonResponse({"error": "Signature verification failed."}, status=400)

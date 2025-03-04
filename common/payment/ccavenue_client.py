from pay_ccavenue import CCAvenue
from .payment_gateway import PaymentGateway


class CCAvenueGateway(PaymentGateway):
    def __init__(self, merchant_code, access_code, working_key):
        self.cca = CCAvenue(
            working_key=working_key,
            access_code=access_code,
            merchant_code=merchant_code,
            redirect_url="YOUR_REDIRECT_URL",
            cancel_url="YOUR_CANCEL_URL"
        )
        self.payment_data = None

    def initialize_payment(self, payment_data):
        """Initialize payment with the given data."""
        self.payment_data = payment_data

    def process_payment(self):
        """Encrypt payment data and return the encrypted request."""
        if not self.payment_data:
            raise ValueError("Payment data not initialized.")
        return self.cca.encrypt(self.payment_data)

    def handle_response(self, response_data):
        """Decrypt and handle the payment response."""
        return self.cca.decrypt(response_data)

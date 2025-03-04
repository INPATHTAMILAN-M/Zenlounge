from abc import ABC, abstractmethod

class PaymentGateway(ABC):
    @abstractmethod
    def initialize_payment(self, payment_data):
        """Initialize payment with the given data."""
        pass

    @abstractmethod
    def process_payment(self):
        """Process the payment."""
        pass

    @abstractmethod
    def handle_response(self, response_data):
        """Handle the payment response."""
        pass

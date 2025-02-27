from rest_framework import viewsets, permissions
from authapp.models import PaymentGateway
from authapp.serializers import PaymentGatewayListSerializer, PaymentGatewayCreateSerializer, PaymentGatewayRetriveSerializer, PaymentGatewayUpdateSerializer

class PaymentGatewayViewSet(viewsets.ModelViewSet):
    queryset = PaymentGateway.objects.all()
    serializer_class = PaymentGatewayListSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'list':
            return PaymentGatewayListSerializer
        elif self.action == 'create':
            return PaymentGatewayCreateSerializer
        elif self.action == 'retrieve':
            return PaymentGatewayRetriveSerializer
        elif self.action in ['update', 'partial_update']:
            return PaymentGatewayUpdateSerializer

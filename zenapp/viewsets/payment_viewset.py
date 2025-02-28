from rest_framework import viewsets, permissions, filters
from ..models import Payment
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

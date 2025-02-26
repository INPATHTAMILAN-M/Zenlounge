from rest_framework import viewsets
from zenapp.models import CustomerSupport
from ..serializers.customer_support_serializer import CustomerSupportGetSerializer, CustomerSupportCreateSerializer, CustomerSupportPatchSerializer, CustomerSupportListSerializer

class CustomerSupportViewSet(viewsets.ModelViewSet):
    queryset = CustomerSupport.objects.all()
    serializer_class = CustomerSupportListSerializer
    http_method_names = ['get', 'post','patch', 'delete']

    def get_serializer_class(self):
        if self.action == 'list':
            return CustomerSupportListSerializer
        elif self.action == 'create':
            return CustomerSupportCreateSerializer
        elif self.action == 'retrieve':
            return CustomerSupportGetSerializer
        elif self.action == 'update' or self.action == 'partial_update':
            return CustomerSupportPatchSerializer

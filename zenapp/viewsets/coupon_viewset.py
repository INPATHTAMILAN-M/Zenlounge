from rest_framework import viewsets, permissions, filters
from ..models import Coupon
from ..serializers.coupon_serializer import CouponGetSerializer, CouponCreateSerializer, CouponPatchSerializer, CouponListSerializer
from ..filters import CouponFilter

class CouponViewSet(viewsets.ModelViewSet):
    queryset = Coupon.objects.all()
    serializer_class = CouponListSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'post','patch', 'delete']
    filterset_class = CouponFilter

    def get_serializer_class(self):
        if self.action == 'list':
            return CouponListSerializer
        elif self.action == 'create':
            return CouponCreateSerializer
        elif self.action == 'retrieve':
            return CouponGetSerializer
        elif self.action == 'update' or self.action == 'partial_update':
            return CouponPatchSerializer

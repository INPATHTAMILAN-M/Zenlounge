from rest_framework import serializers
from zenapp.models import Coupon

class CouponGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = '__all__'

class CouponCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = '__all__'

class CouponPatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = '__all__'

class CouponListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = '__all__'

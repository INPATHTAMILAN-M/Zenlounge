from rest_framework import serializers
from  zenapp.models import CustomerSupport

class CustomerSupportGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerSupport
        fields = '__all__'

class CustomerSupportCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerSupport
        fields = '__all__'

class CustomerSupportPatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerSupport
        fields = '__all__'

class CustomerSupportListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerSupport
        fields = '__all__'

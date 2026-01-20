from rest_framework import serializers
from .models import Vendor

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ['id', 'user', 'shop_name', 'description', 'is_verified', 'created_at']
        read_only_fields = ['user', 'is_verified', 'created_at']

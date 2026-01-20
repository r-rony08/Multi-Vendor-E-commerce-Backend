from rest_framework import serializers
from .models import CartItem
from decimal import Decimal

class CartItemSerializer(serializers.ModelSerializer):
    """
    Serializer for cart items.
    - Calculates total price
    - Shows vendor name and product info
    """
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_price = serializers.DecimalField(source='product.price', max_digits=12, decimal_places=2, read_only=True)
    total_price = serializers.SerializerMethodField()
    vendor_name = serializers.CharField(source='product.vendor.shop_name', read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'user', 'product', 'product_name', 'vendor_name', 'product_price', 'quantity', 'total_price']
        read_only_fields = ['user', 'product_name', 'product_price', 'total_price', 'vendor_name']

    def get_total_price(self, obj):
        return obj.total_price

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than zero.")

        product = self.initial_data.get('product')
        if product and hasattr(product, 'stock') and value > product.stock:
            raise serializers.ValidationError("Quantity exceeds available stock.")
        return value

    def create(self, validated_data):
        """
        Assign the logged-in user automatically.
        """
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)

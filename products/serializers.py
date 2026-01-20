from rest_framework import serializers
from .models import Product
from vendors.models import Vendor
from rest_framework.exceptions import ValidationError
from django.utils.text import slugify

class ProductSerializer(serializers.ModelSerializer):
    """
    Product serializer:
    - Validates stock, price
    - Ensures SKU uniqueness per vendor
    - Shows vendor_name & category_name
    """
    vendor_name = serializers.CharField(source='vendor.shop_name', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'vendor', 'vendor_name', 'category', 'category_name',
            'name', 'slug', 'sku', 'price', 'stock', 'is_active',
            'created_at', 'updated_at', 'deleted_at',
        ]
        read_only_fields = ['vendor', 'created_at', 'updated_at', 'deleted_at', 'slug']

    def validate_vendor(self, value):
        """
        Ensure vendor belongs to request.user
        """
        request = self.context.get('request')
        if request and value.user != request.user:
            raise ValidationError("You can only create products for your own vendor profile.")
        if value.deleted_at:
            raise ValidationError("Cannot add products to a deleted vendor profile.")
        return value

    def validate_category(self, value):
        if value and (not value.is_active or value.deleted_at):
            raise ValidationError("Cannot assign product to inactive/deleted category.")
        return value

    def validate_price(self, value):
        if value < 0:
            raise ValidationError("Price must be >= 0.")
        return value

    def validate_stock(self, value):
        if value < 0:
            raise ValidationError("Stock must be >= 0.")
        return value

    def validate(self, attrs):
        """
        Ensure SKU is unique per vendor
        """
        vendor = attrs.get('vendor') or (self.instance.vendor if self.instance else None)
        sku = attrs.get('sku')
        if vendor and sku:
            qs = Product.objects.filter(vendor=vendor, sku__iexact=sku)
            if self.instance:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise ValidationError("SKU must be unique for this vendor.")
        return attrs

    def create(self, validated_data):
        validated_data['slug'] = slugify(validated_data['name'])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data.pop('vendor', None)
        validated_data.pop('deleted_at', None)
        validated_data.pop('slug', None)
        return super().update(instance, validated_data)

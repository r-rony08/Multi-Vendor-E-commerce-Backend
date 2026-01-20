from rest_framework import serializers
from .models import Vendor
from users.models import User
from rest_framework.exceptions import ValidationError

class VendorSerializer(serializers.ModelSerializer):
    """
    Vendor serializer with validation.
    Ensures:
    - Only users with VENDOR role can create
    - Prevents overwriting sensitive fields
    """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    status = serializers.CharField(read_only=True)

    class Meta:
        model = Vendor
        fields = [
            "id", "user", "shop_name", "description",
            "status", "is_verified", "commission_rate",
            "created_at", "updated_at",
        ]
        read_only_fields = ["user", "status", "is_verified", "commission_rate", "created_at", "updated_at"]

    def validate_user(self, value):
        if value.role != User.Role.VENDOR:
            raise ValidationError("Only users with VENDOR role can create a vendor profile.")
        return value

    def validate_shop_name(self, value):
        value = value.strip()
        if Vendor.objects.filter(shop_name__iexact=value).exists():
            raise ValidationError("Shop name already exists.")
        return value

    def create(self, validated_data):
        validated_data["status"] = Vendor.Status.PENDING
        validated_data["is_verified"] = False
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Prevent sensitive fields updates
        validated_data.pop("is_verified", None)
        validated_data.pop("status", None)
        validated_data.pop("commission_rate", None)
        return super().update(instance, validated_data)

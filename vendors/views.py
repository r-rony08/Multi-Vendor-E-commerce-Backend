from django.db import transaction
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError, NotFound

from .models import Vendor
from .serializers import VendorSerializer
from .permissions import IsVendorUser

class VendorCreateView(CreateAPIView):
    """
    Vendor onboarding.
    Only users with role=VENDOR.
    """
    serializer_class = VendorSerializer
    permission_classes = [IsAuthenticated, IsVendorUser]
    throttle_scope = "auth"

    @transaction.atomic
    def perform_create(self, serializer):
        user = self.request.user
        if hasattr(user, "vendor_profile"):
            raise ValidationError("Vendor profile already exists for this user.")
        serializer.save(user=user)


class VendorProfileView(RetrieveUpdateAPIView):
    """
    Retrieve / Update vendor profile.
    Owners only; admins bypass.
    """
    serializer_class = VendorSerializer
    permission_classes = [IsAuthenticated, IsVendorUser]
    throttle_scope = "auth"

    def get_object(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            vendor_id = self.request.query_params.get("vendor_id")
            if not vendor_id:
                raise ValidationError("vendor_id query parameter required for admins.")
            try:
                return Vendor.objects.get(id=vendor_id)
            except Vendor.DoesNotExist:
                raise NotFound("Vendor not found.")
        # Owner access
        try:
            vendor = user.vendor_profile
        except Vendor.DoesNotExist:
            raise NotFound("Vendor profile not found.")
        if vendor.deleted_at:
            raise NotFound("Vendor profile is deleted.")
        return vendor

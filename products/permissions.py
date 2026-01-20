from rest_framework.permissions import BasePermission, SAFE_METHODS
from users.models import User

class IsVendorOrReadOnly(BasePermission):
    """
    Only vendors can create/update/delete products.
    Admins bypass.
    Others can only read (GET, HEAD, OPTIONS).
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        user = request.user
        if not user or not user.is_authenticated:
            return False
        if user.is_staff or user.is_superuser:
            return True
        return user.role == User.Role.VENDOR

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        user = request.user
        if user.is_staff or user.is_superuser:
            return True
        return hasattr(obj, 'vendor') and obj.vendor.user == user

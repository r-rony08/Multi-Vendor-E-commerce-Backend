from rest_framework.permissions import BasePermission
from users.models import User

class IsVendorUser(BasePermission):
    """
    Permission:
    - Allow access only to users with VENDOR role.
    - Admins (is_staff or is_superuser) bypass this check.
    """

    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        if user.is_staff or user.is_superuser:
            return True
        return user.role == User.Role.VENDOR and user.is_active

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.is_staff or user.is_superuser:
            return True
        return hasattr(obj, "user") and obj.user == user

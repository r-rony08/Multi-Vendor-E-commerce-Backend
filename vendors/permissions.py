from rest_framework.permissions import BasePermission

class IsVendorUser(BasePermission):
    """
    Allow access only if user role is VENDOR
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'VENDOR'

    def has_object_permission(self, request, view, obj):
        # Only owner can edit
        return obj.user == request.user

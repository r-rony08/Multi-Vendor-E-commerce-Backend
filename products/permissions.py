from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsVendorOrReadOnly(BasePermission):
    """
    Only vendors can create/update/delete their own products.
    Others can only view (GET).
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.role == 'VENDOR'

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.vendor.user == request.user

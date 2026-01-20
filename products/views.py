from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.exceptions import ValidationError
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from .models import Product
from .serializers import ProductSerializer
from .permissions import IsVendorOrReadOnly
from .pagination import ProductCursorPagination

@method_decorator(cache_page(60*5), name='dispatch')
class ProductListCreateView(ListCreateAPIView):
    """
    List & Create products.
    Public can view only active products.
    Vendors can create products.
    Admins bypass.
    """
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsVendorOrReadOnly]
    pagination_class = ProductCursorPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category__slug', 'vendor__id', 'is_active']
    search_fields = ['name', 'sku', 'description']
    ordering_fields = ['price', 'created_at']
    throttle_scope = 'auth'

    def get_queryset(self):
        qs = Product.objects.filter(is_active=True, deleted_at__isnull=True).select_related('vendor', 'category')
        user = self.request.user
        if user.is_authenticated and (user.is_staff or user.is_superuser):
            return Product.objects.all().select_related('vendor', 'category')
        return qs

    def perform_create(self, serializer):
        user = self.request.user
        if not hasattr(user, 'vendor_profile'):
            raise ValidationError("You must have a vendor profile to add products.")
        serializer.save(vendor=user.vendor_profile)


class ProductDetailView(RetrieveUpdateDestroyAPIView):
    """
    Retrieve, Update, Delete a product.
    Restricted to owner vendors; Admins bypass.
    """
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsVendorOrReadOnly]
    throttle_scope = 'auth'

    def get_queryset(self):
        user = self.request.user
        qs = Product.objects.filter(deleted_at__isnull=True).select_related('vendor', 'category')
        if user.is_authenticated and (user.is_staff or user.is_superuser):
            return Product.objects.all().select_related('vendor', 'category')
        elif user.is_authenticated and hasattr(user, 'vendor_profile'):
            return qs.filter(vendor=user.vendor_profile)
        else:
            return qs.filter(is_active=True)

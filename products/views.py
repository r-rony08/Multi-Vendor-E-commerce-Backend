from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from rest_framework import filters

from .models import Product
from .serializers import ProductSerializer
from .permissions import IsVendorOrReadOnly
from .pagination import ProductCursorPagination
from django_filters.rest_framework import DjangoFilterBackend

# Create your views here.

# List & Create Products
@method_decorator(cache_page(60*5), name='dispatch')  # cache list for 5 mins
class ProductListCreateView(ListCreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsVendorOrReadOnly]
    pagination_class = ProductCursorPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category__id', 'vendor__id', 'is_active']
    search_fields = ['name']
    ordering_fields = ['price', 'created_at']

    def get_queryset(self):
        return Product.objects.filter(is_active=True)

    def perform_create(self, serializer):
        # Automatically link product to logged-in vendor
        serializer.save(vendor=self.request.user.vendor)


# Retrieve, Update, Delete single Product
class ProductDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsVendorOrReadOnly]
    queryset = Product.objects.all()
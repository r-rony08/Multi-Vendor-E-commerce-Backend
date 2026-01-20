from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import serializers
from .models import CartItem
from .serializers import CartItemSerializer
from decimal import Decimal

class CartItemListCreateView(ListCreateAPIView):
    """
    List all cart items for the current user.
    Add new items to the cart.
    """
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(
            user=self.request.user, 
            product__is_active=True, 
            deleted_at__isnull=True
        ).select_related("product", "product__vendor")

    def perform_create(self, serializer):
        product = serializer.validated_data["product"]
        quantity = serializer.validated_data.get("quantity", 1)

        if not product.is_active or product.deleted_at:
            raise serializers.ValidationError(f"Product '{product.name}' is not available.")

        if quantity > product.stock:
            raise serializers.ValidationError(
                f"Quantity exceeds available stock for '{product.name}'."
            )

        serializer.save(user=self.request.user)


class CartItemDetailView(RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or soft-delete a cart item.
    Only accessible to the owner.
    """
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user).select_related(
            "product", "product__vendor"
        )

    def perform_update(self, serializer):
        product = serializer.validated_data.get("product", serializer.instance.product)
        quantity = serializer.validated_data.get("quantity", serializer.instance.quantity)

        if not product.is_active or product.deleted_at:
            raise serializers.ValidationError(f"Product '{product.name}' is not available.")

        if quantity > product.stock:
            raise serializers.ValidationError(
                f"Quantity exceeds available stock for '{product.name}'."
            )

        serializer.save()


class CartSummaryView(APIView):
    """
    Get total items and total price for the current user's cart.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart_items = CartItem.objects.filter(
            user=request.user, 
            product__is_active=True,
            deleted_at__isnull=True
        ).select_related("product", "product__vendor")

        total_price = sum(
            item.total_price for item in cart_items
        ) or Decimal('0')

        return Response({
            "total_items": cart_items.count(),
            "total_price": total_price,
        })

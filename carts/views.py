from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from .models import CartItem
from rest_framework import serializers
from .serializers import CartItemSerializer
from analytics.serializers_utils import CartSummarySerializer

class CartItemListCreateView(ListCreateAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]
 

    def get_queryset(self):
        # Remove inactive products automatically
        CartItem.objects.filter(user=self.request.user, product__is_active=False).delete()
        return CartItem.objects.filter(user=self.request.user).select_related('product')

    def perform_create(self, serializer):
        product = serializer.validated_data['product']
        quantity = serializer.validated_data.get('quantity', 1)
        
        if quantity > product.stock:
            raise serializers.ValidationError("Quantity exceeds available stock.")

        serializer.save(user=self.request.user)


class CartItemDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user).select_related('product')
    
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class CartSummaryView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CartSummarySerializer

    def get(self, request):
        cart_items = CartItem.objects.filter(user=request.user).select_related('product')
        total_price = sum(item.quantity * item.product.price for item in cart_items)
        return Response({
            "total_items": cart_items.count(),
            "total_price": total_price
        })


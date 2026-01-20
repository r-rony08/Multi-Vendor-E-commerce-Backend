from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from .serializers import OrderCreateSerializer
from rest_framework.views import APIView
from orders.models import Order
from analytics.serializers_utils import RefundSerializer

class OrderCreateView(GenericAPIView):
    serializer_class = OrderCreateSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.get_serializer()
        order = serializer.save()
        return Response(
            {
                "order_id": order.id,
                "total_price": order.total_price,
                "status": order.status
            },
            status=status.HTTP_201_CREATED
        )

class RefundOrderView(APIView):
    """
    Refund an order and restore stock
    """
    permission_classes = [IsAdminUser]
    serializer_class = RefundSerializer

    def post(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id)
            if order.status not in ['PAID', 'SHIPPED']:
                return Response({"error": "Order cannot be refunded"}, status=400)

            # Restore stock
            for item in order.items.all():
                product = item.product
                product.stock += item.quantity
                product.save()

            # Update order status
            order.status = 'REFUNDED'
            order.save()

            return Response({"message": f"Order {order.id} refunded successfully"})
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=404)
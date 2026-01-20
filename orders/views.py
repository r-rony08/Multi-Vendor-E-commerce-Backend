from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.db import transaction
from django.shortcuts import get_object_or_404
from .models import Order
from .serializers import OrderCreateSerializer

class OrderCreateView(CreateAPIView):
    """
    Convert a user's cart into an Order.
    Atomic, multi-vendor, stock-checked.
    """
    serializer_class = OrderCreateSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        return {"request": self.request}


class OrderListView(ListAPIView):
    """
    List orders for the current user.
    Admins see all orders.
    """
    serializer_class = OrderCreateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return Order.objects.all()
        return Order.objects.filter(user=user)


class RefundOrderView(APIView):
    """
    Refund an order and restore stock.
    Admin-only, atomic.
    """
    permission_classes = [IsAdminUser]

    def post(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)

        if order.status not in [Order.Status.PAID, Order.Status.SHIPPED]:
            return Response({"error": f"Order cannot be refunded (status={order.status})"},
                            status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            for item in order.items.select_related("product").all():
                product = item.product
                if product.deleted_at or not product.is_active:
                    continue
                product.stock += item.quantity
                product.save(update_fields=["stock"])

            order.status = Order.Status.CANCELLED
            order.save(update_fields=["status", "updated_at"])

        return Response({"message": f"Order {order.id} refunded successfully"},
                        status=status.HTTP_200_OK)

from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from django.db.models import Sum, Count, F
from orders.models import Order
from analytics.serializers_utils import AdminAnalyticsSerializer

class AdminAnalyticsView(GenericAPIView):
    """
    Admin dashboard analytics.
    Provides total orders, total revenue, per-vendor stats, and order status distribution.
    """
    permission_classes = [IsAdminUser]
    serializer_class = AdminAnalyticsSerializer  # Dummy serializer for Swagger

    def get(self, request):
        # Total orders
        total_orders = Order.objects.count()

        # Total revenue (only PAID orders)
        total_revenue = (
            Order.objects.filter(status=Order.Status.PAID)
            .aggregate(total=Sum('total_price'))['total'] or 0
        )

        # Orders and revenue per vendor
        orders_per_vendor = (
            Order.objects.filter(status=Order.Status.PAID)
            .values('items__product__vendor__shop_name')
            .annotate(
                total_orders=Count('id', distinct=True),
                total_revenue=Sum(F('items__price') * F('items__quantity'))
            )
            .order_by('-total_revenue')
        )

        # Orders by status
        orders_by_status = (
            Order.objects.values('status')
            .annotate(count=Count('id'))
            .order_by('status')
        )

        return Response({
            "total_orders": total_orders,
            "total_revenue": total_revenue,
            "orders_per_vendor": list(orders_per_vendor),
            "orders_by_status": list(orders_by_status)
        })

from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from django.db.models import Sum, Count
from orders.models import Order
from products.models import Product
from vendors.models import Vendor
from analytics.serializers_utils import AdminAnalyticsSerializer

class AdminAnalyticsView(GenericAPIView):
    """
    Admin dashboard analytics
    """
    permission_classes = [IsAdminUser]
    serializer_class = AdminAnalyticsSerializer  # define dummy serializer

    def get(self, request):
        total_orders = Order.objects.count()
        total_revenue = Order.objects.filter(status='PAID').aggregate(Sum('total_price'))['total_price__sum'] or 0

        # Orders per vendor
        orders_per_vendor = (
            Order.objects
            .filter(status='PAID')
            .values('items__product__vendor__shop_name')
            .annotate(count=Count('id'), revenue=Sum('total_price'))
        )

        # Orders per status
        orders_by_status = (
            Order.objects
            .values('status')
            .annotate(count=Count('id'))
        )

        return Response({
            "total_orders": total_orders,
            "total_revenue": total_revenue,
            "orders_per_vendor": list(orders_per_vendor),
            "orders_by_status": list(orders_by_status)
        })

# all reusable dummy serializers

from rest_framework import serializers

# Logout
class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

# Cart summary
class CartSummarySerializer(serializers.Serializer):
    total_items = serializers.IntegerField()
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2)

# Admin analytics
class AdminAnalyticsSerializer(serializers.Serializer):
    total_orders = serializers.IntegerField()
    total_revenue = serializers.DecimalField(max_digits=12, decimal_places=2)
    orders_per_vendor = serializers.DictField(child=serializers.IntegerField())

# Refund
class RefundSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()

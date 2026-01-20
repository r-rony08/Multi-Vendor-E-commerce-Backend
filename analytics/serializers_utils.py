from rest_framework import serializers

class AdminAnalyticsSerializer(serializers.Serializer):
    total_orders = serializers.IntegerField()
    total_revenue = serializers.DecimalField(max_digits=12, decimal_places=2)
    orders_per_vendor = serializers.ListField()
    orders_by_status = serializers.ListField()


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

class CartSummarySerializer(serializers.Serializer):
    total_items = serializers.IntegerField()
    total_price = serializers.DecimalField(max_digits=12, decimal_places=2)

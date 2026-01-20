from rest_framework import serializers
from orders.models import Order
from .models import Payment
from decimal import Decimal
from django.shortcuts import get_object_or_404

class PaymentInitSerializer(serializers.Serializer):
    """
    Initialize a payment for an order.
    """
    order_id = serializers.IntegerField()

    def validate_order_id(self, value):
        order = get_object_or_404(Order, id=value)
        if order.status != Order.Status.PENDING:
            raise serializers.ValidationError("Only pending orders can be paid.")
        if hasattr(order, 'payment'):
            raise serializers.ValidationError("Payment already initiated for this order.")
        return value

    def create(self, validated_data):
        order = get_object_or_404(Order, id=validated_data['order_id'])
        payment = Payment.objects.create(
            order=order,
            amount=order.total_price or Decimal('0'),
            gateway='STRIPE_SANDBOX',
        )
        return payment


class PaymentWebhookSerializer(serializers.Serializer):
    """
    Process payment gateway webhooks.
    """
    payment_id = serializers.IntegerField()
    status = serializers.ChoiceField(choices=["success", "failed"])

    def validate_status(self, value):
        return value.upper()

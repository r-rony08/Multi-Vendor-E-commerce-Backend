from rest_framework import serializers
from orders.models import Order
from .models import Payment

class PaymentInitSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()

    def create(self, validated_data):
        order = Order.objects.get(id=validated_data['order_id'])

        if hasattr(order, 'payment'):
            raise serializers.ValidationError("Payment already initiated for this order")

        payment = Payment.objects.create(
            order=order,
            amount=order.total_price,
            gateway='STRIPE_SANDBOX'
        )
        return payment


class PaymentWebhookSerializer(serializers.Serializer):
    payment_id = serializers.IntegerField()
    status = serializers.ChoiceField(choices=["success", "failed"])

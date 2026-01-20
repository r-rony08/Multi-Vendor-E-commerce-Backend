from rest_framework import serializers
from django.db import transaction
from carts.models import CartItem
from products.models import Product
from .models import Order, OrderItem

class OrderCreateSerializer(serializers.Serializer):

    def create(self, validated_data):
        user = self.context['request'].user
        cart_items = CartItem.objects.filter(user=user)

        if not cart_items.exists():
            raise serializers.ValidationError("Cart is empty")

        with transaction.atomic():
            order = Order.objects.create(user=user)
            total = 0

            for item in cart_items:
                product = Product.objects.select_for_update().get(id=item.product.id)

                if product.stock < item.quantity:
                    raise serializers.ValidationError(
                        f"Not enough stock for {product.name}"
                    )

                product.stock -= item.quantity
                product.save()

                OrderItem.objects.create(
                    order=order,
                    product=product,
                    price=product.price,
                    quantity=item.quantity
                )

                total += product.price * item.quantity

            order.total_price = total
            order.save()

            cart_items.delete()

        return order

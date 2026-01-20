from rest_framework import serializers
from django.db import transaction
from carts.models import CartItem
from products.models import Product
from .models import Order, OrderItem
from decimal import Decimal

class OrderCreateSerializer(serializers.Serializer):
    """
    Convert a user's cart into an Order.
    Handles stock check, multi-vendor, and atomic transaction.
    """

    def create(self, validated_data):
        user = self.context["request"].user

        # Fetch cart items
        cart_items = CartItem.objects.filter(user=user).select_related("product", "product__vendor")
        if not cart_items.exists():
            raise serializers.ValidationError("Cart is empty.")

        with transaction.atomic():
            order = Order.objects.create(user=user)
            total = Decimal('0')

            for item in cart_items:
                product = Product.objects.select_for_update().get(id=item.product.id)

                if product.deleted_at or not product.is_active:
                    raise serializers.ValidationError(f"Product '{product.name}' is unavailable.")
                if product.stock < item.quantity:
                    raise serializers.ValidationError(
                        f"Not enough stock for '{product.name}'. Requested {item.quantity}, Available {product.stock}"
                    )

                # Deduct stock
                product.stock -= item.quantity
                product.save(update_fields=["stock"])

                # Create order item
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    vendor=product.vendor,
                    price=product.price,
                    quantity=item.quantity
                )

                total += product.price * item.quantity

            order.total_price = total
            order.save(update_fields=["total_price"])

            # Clear user's cart
            cart_items.delete()

        return order

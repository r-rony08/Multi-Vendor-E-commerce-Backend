from django.db import models
from django.conf import settings
from django.utils import timezone
from products.models import Product
from vendors.models import Vendor
from decimal import Decimal

User = settings.AUTH_USER_MODEL

class Order(models.Model):
    """
    Represents a customer's order.
    Multi-vendor compatible.
    """
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        PAID = "PAID", "Paid"
        SHIPPED = "SHIPPED", "Shipped"
        COMPLETED = "COMPLETED", "Completed"
        CANCELLED = "CANCELLED", "Cancelled"

    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='orders')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING, db_index=True)
    total_price = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True, db_index=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["user"]),
        ]

    def calculate_total(self):
        """
        Recalculate total price from order items.
        """
        total = sum(item.price * item.quantity for item in self.items.all())
        self.total_price = total
        self.save(update_fields=["total_price"])
        return self.total_price

    def soft_delete(self):
        """
        Soft-delete the order.
        """
        self.deleted_at = timezone.now()
        self.save(update_fields=["deleted_at"])

    def __str__(self):
        return f"Order #{self.id} ({self.user})"


class OrderItem(models.Model):
    """
    Individual item in an order.
    Linked to product and vendor for multi-vendor marketplaces.
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    vendor = models.ForeignKey(Vendor, on_delete=models.PROTECT)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, blank=True, db_index=True)

    class Meta:
        indexes = [
            models.Index(fields=["product"]),
            models.Index(fields=["vendor"]),
        ]

    def save(self, *args, **kwargs):
        if self.quantity <= 0:
            raise ValueError("Quantity must be greater than 0")
        if self.price < 0:
            raise ValueError("Price cannot be negative")
        if not self.vendor_id and self.product_id:
            self.vendor = self.product.vendor
        super().save(*args, **kwargs)

    def soft_delete(self):
        self.deleted_at = timezone.now()
        self.save(update_fields=["deleted_at"])

    def __str__(self):
        return f"{self.product.name} x {self.quantity} (Order #{self.order.id})"

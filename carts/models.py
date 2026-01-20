from django.db import models
from django.conf import settings
from django.utils import timezone
from products.models import Product
from decimal import Decimal

User = settings.AUTH_USER_MODEL

class CartItem(models.Model):
    """
    Represents an item in a user's cart.
    Multi-vendor safe; unique per product per user.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cart_items", db_index=True)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, blank=True, db_index=True)

    class Meta:
        unique_together = ("user", "product")
        ordering = ["-added_at"]
        indexes = [
            models.Index(fields=["user", "deleted_at"]),
        ]

    def __str__(self):
        return f"{self.user} - {self.product}"

    @property
    def total_price(self):
        """
        Total price for this cart item.
        Returns Decimal('0') if product is inactive or deleted.
        """
        if self.product.deleted_at or not self.product.is_active:
            return Decimal('0')
        return self.quantity * self.product.price

    def soft_delete(self):
        """
        Soft-delete the cart item without removing from DB.
        """
        self.deleted_at = timezone.now()
        self.save(update_fields=["deleted_at"])

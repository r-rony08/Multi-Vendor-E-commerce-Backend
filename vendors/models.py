from django.db import models
from django.conf import settings
from django.utils import timezone

User = settings.AUTH_USER_MODEL

class Vendor(models.Model):
    """
    Vendor profile linked to a user.
    Multi-vendor safe and trackable.
    """
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending Approval"
        APPROVED = "APPROVED", "Approved"
        SUSPENDED = "SUSPENDED", "Suspended"

    user = models.OneToOneField(
        User,
        on_delete=models.PROTECT,
        related_name="vendor_profile"
    )
    shop_name = models.CharField(max_length=255, unique=True, db_index=True)
    description = models.TextField(blank=True, max_length=1000)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING, db_index=True)
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2, default=10.00,
                                          help_text="Platform commission percentage")
    is_verified = models.BooleanField(default=False, help_text="KYC / document verification")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "vendors"
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["is_verified"]),
        ]

    def soft_delete(self):
        self.deleted_at = timezone.now()
        self.save(update_fields=["deleted_at"])

    def __str__(self):
        return f"{self.shop_name} ({self.user.email})"

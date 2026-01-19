from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    ROLE_CHOICES = (
        ('ADMIN', 'Admin'),
        ('VENDOR', 'Vendor'),
        ('CUSTOMER', 'Customer'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='CUSTOMER')

    def __str__(self):
        return self.username

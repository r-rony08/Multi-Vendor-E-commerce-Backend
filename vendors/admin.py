from django.contrib import admin
from .models import Vendor

@admin.register(Vendor)

class VendorAdmin(admin.ModelAdmin):
    list_display = ['shop_name', 'user', 'is_verified', 'created_at']
    list_filter = ['is_verified', 'created_at']
    search_fields = ['shop_name', 'user__username']

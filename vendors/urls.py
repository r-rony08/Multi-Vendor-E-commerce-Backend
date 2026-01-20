from django.urls import path
from .views import VendorCreateView, VendorProfileView

urlpatterns = [
    path('create/', VendorCreateView.as_view(), name='vendor-create'),
    path('profile/', VendorProfileView.as_view(), name='vendor-profile'),
]

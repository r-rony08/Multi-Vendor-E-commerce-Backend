from django.urls import path
from .views import VendorCreateView, VendorProfileView

app_name = "vendors"

urlpatterns = [
    path("create/", VendorCreateView.as_view(), name="vendor-create"),
    path("me/", VendorProfileView.as_view(), name="vendor-profile"),
]

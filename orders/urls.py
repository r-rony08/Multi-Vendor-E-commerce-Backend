from django.urls import path
from .views import OrderCreateView, OrderListView, RefundOrderView

app_name = "orders"

urlpatterns = [
    path("", OrderCreateView.as_view(), name="order-create"),
    path("my/", OrderListView.as_view(), name="order-list"),
    path("<int:order_id>/refund/", RefundOrderView.as_view(), name="order-refund"),
]

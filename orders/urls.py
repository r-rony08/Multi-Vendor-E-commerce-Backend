from django.urls import path
from .views import OrderCreateView, RefundOrderView

urlpatterns = [
    path('orders/create/', OrderCreateView.as_view(), name='order-create'),
    path('orders/<int:order_id>/refund/', RefundOrderView.as_view(), name='order-refund'),
]

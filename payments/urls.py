from django.urls import path
from .views import PaymentInitView
from .webhooks import PaymentWebhookView

urlpatterns = [
    path('payments/init/', PaymentInitView.as_view(), name='payment-init'),
    path('payments/webhook/', PaymentWebhookView.as_view(), name='payment-webhook'),
]

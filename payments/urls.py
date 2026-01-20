from django.urls import path
from .views import PaymentInitView
from .webhooks import PaymentWebhookView

app_name = "payments"

urlpatterns = [
    path("init/", PaymentInitView.as_view(), name="payment-init"),
    path("webhook/", PaymentWebhookView.as_view(), name="payment-webhook"),
]

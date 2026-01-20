from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .serializers import PaymentInitSerializer, PaymentWebhookSerializer
from .models import Payment

class PaymentInitView(GenericAPIView):
    """
    Initialize a payment for an order.
    """
    serializer_class = PaymentInitSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payment = serializer.save()

        # In production, return real gateway URL or token
        return Response({
            "payment_id": payment.id,
            "payment_url": "https://sandbox-payment-gateway.com/pay"
        }, status=status.HTTP_201_CREATED)


class PaymentWebhookView(GenericAPIView):
    """
    Receive payment gateway webhooks.
    Public endpoint; no authentication.
    """
    serializer_class = PaymentWebhookSerializer
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        payment_id = serializer.validated_data["payment_id"]
        status_value = serializer.validated_data["status"].upper()

        payment = get_object_or_404(Payment, id=payment_id)
        order = payment.order

        # Idempotency: ignore if already processed
        if payment.status in ["SUCCESS", "FAILED"]:
            return Response({"message": "Payment already processed."}, status=status.HTTP_200_OK)

        if status_value == "SUCCESS":
            payment.status = "SUCCESS"
            order.status = Order.Status.PAID
        else:
            payment.status = "FAILED"
            order.status = Order.Status.CANCELLED

        payment.save(update_fields=["status", "updated_at"])
        order.save(update_fields=["status", "updated_at"])

        return Response({"message": "Webhook processed"}, status=status.HTTP_200_OK)

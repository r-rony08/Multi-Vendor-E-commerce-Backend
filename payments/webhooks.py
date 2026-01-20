from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import PaymentWebhookSerializer
from .models import Payment

class PaymentWebhookView(GenericAPIView):
    serializer_class = PaymentWebhookSerializer
    authentication_classes = []  # webhook usually public
    permission_classes = []      # allow external POST

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        payment_id = serializer.validated_data["payment_id"]
        status_value = serializer.validated_data["status"]

        payment = Payment.objects.get(id=payment_id)
        order = payment.order

        if status_value == "success":
            payment.status = "SUCCESS"
            order.status = "PAID"
        else:
            payment.status = "FAILED"
            order.status = "CANCELLED"

        payment.save()
        order.save()

        return Response({"message": "Webhook processed"}, status=status.HTTP_200_OK)

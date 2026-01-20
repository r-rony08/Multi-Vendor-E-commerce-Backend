from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import PaymentInitSerializer
from .models import Payment

class PaymentInitView(GenericAPIView):
    serializer_class = PaymentInitSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        payment = serializer.save()
        # Normally, here you'd generate a payment URL/token for sandbox
        return Response(
            {
                "payment_id": payment.id,
                "payment_url": "https://sandbox-payment-gateway.com/pay"
            },
            status=status.HTTP_201_CREATED
        )

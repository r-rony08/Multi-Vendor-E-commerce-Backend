from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from .models import Vendor
from .serializers import VendorSerializer
from .permissions import IsVendorUser

# Vendor profile creation (role=VENDOR only)
class VendorCreateView(CreateAPIView):
    serializer_class = VendorSerializer
    permission_classes = [IsAuthenticated, IsVendorUser]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# Vendor profile view/update
class VendorProfileView(RetrieveUpdateAPIView):
    serializer_class = VendorSerializer
    permission_classes = [IsAuthenticated, IsVendorUser]

    def get_object(self):
        return self.request.user.vendor

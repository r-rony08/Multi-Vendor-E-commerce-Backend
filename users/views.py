from django.db import transaction
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication

from .serializers import UserRegisterSerializer, UserProfileSerializer
from analytics.serializers_utils import LogoutSerializer

class UserRegisterView(CreateAPIView):
    """
    Register a new user
    """
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]
    throttle_scope = "auth"

    @transaction.atomic
    def perform_create(self, serializer):
        serializer.save()

class UserProfileView(RetrieveUpdateAPIView):
    """
    Get / Update profile
    """
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_object(self):
        return self.request.user

class LoginView(TokenObtainPairView):
    """
    JWT Login
    """
    permission_classes = [AllowAny]
    throttle_scope = "auth"

class LogoutView(APIView):
    """
    Logout by blacklisting refresh token
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = LogoutSerializer
    throttle_scope = "auth"

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        refresh = serializer.validated_data.get("refresh")
        try:
            token = RefreshToken(refresh)
            token.blacklist()
        except Exception:
            pass

        return Response({"detail": "Successfully logged out"}, status=status.HTTP_200_OK)

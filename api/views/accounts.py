from django.contrib.auth import get_user_model
from rest_framework import generics, permissions

from api.serializers.accounts import MeSerializer, RegisterSerializer

User = get_user_model()


class RegisterAPIView(generics.CreateAPIView):
    """
    Handle POST /api/auth/register/.

    Creates a new customer account. This endpoint is public because
    unauthenticated users must be able to register.
    """

    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class MeAPIView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MeSerializer

    def get_object(self):
        return self.request.user
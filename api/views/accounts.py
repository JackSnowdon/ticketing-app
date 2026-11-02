from django.contrib.auth import get_user_model
from rest_framework import generics, permissions

from api.serializers.accounts import RegisterSerializer

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
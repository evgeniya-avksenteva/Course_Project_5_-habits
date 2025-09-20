from rest_framework import generics
from rest_framework.permissions import AllowAny

from .serializers import RegisterSerializer


class RegisterAPIView(generics.CreateAPIView):
    """Представление для регистрации нового пользователя."""

    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

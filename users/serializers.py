from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer

User = get_user_model()


class RegisterSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        """Создаёт нового пользователя с помощью метода менеджера create_user."""

        password = validated_data.pop("password")  # достаём пароль
        user = User.objects.create_user(**validated_data, password=password)
        return user

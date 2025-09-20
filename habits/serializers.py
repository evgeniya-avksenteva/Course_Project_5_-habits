from rest_framework import serializers

from .models import Habit


class HabitSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Habit. Используется для преобразования данных привычек в JSON и обратно.
    Все поля модели включены. Поле 'user' доступно только для чтения."""

    class Meta:
        model = Habit
        fields = "__all__"
        read_only_fields = ("user",)

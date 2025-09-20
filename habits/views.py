from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, mixins, permissions, viewsets
from rest_framework.permissions import AllowAny

from .models import Habit
from .paginators import HabitPagination
from .permissions import IsOwnerOrReadOnlyForPublic
from .serializers import HabitSerializer


# Список публичных привычек (только чтение)
class PublicHabitListAPIView(generics.ListAPIView):
    """API для получения списка публичных привычек. Доступ разрешён для всех пользователей.
    Используется пагинация и сериализация HabitSerializer."""

    serializer_class = HabitSerializer
    pagination_class = HabitPagination
    permission_classes = [AllowAny]

    def get_queryset(self):
        """Возвращает queryset с фильтрацией только публичных привычек."""
        return Habit.objects.filter(is_public=True)


# CRUD для привычек текущего пользователя с пагинацией
class HabitViewSet(viewsets.ModelViewSet):
    """Вьюсет CRUD для привычек пользователей с правами"""

    serializer_class = HabitSerializer
    pagination_class = HabitPagination
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnlyForPublic]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["is_public"]

    def get_queryset(self):
        """Возвращает все привычки сортированные по id. Проверка доступа происходит в permission-классе."""

        return Habit.objects.all().order_by("id")

    def perform_create(self, serializer):
        """При создании привычки автоматически устанавливает пользователя из запроса."""
        serializer.save(user=self.request.user)


class MyHabitViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    """Вьюсет для CRUD операций только со своими привычками текущего пользователя.
    Доступ открыт только для авторизованных пользователей."""

    serializer_class = HabitSerializer
    pagination_class = HabitPagination
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """Возвращает привычки текущего пользователя, сортированные по id."""

        serializer.save(user=self.request.user)

    def get_queryset(self):
        """При создании привычки сохраняет связь с текущим пользователем."""

        return Habit.objects.filter(user=self.request.user).order_by("id")

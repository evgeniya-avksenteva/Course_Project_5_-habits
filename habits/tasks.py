from datetime import timedelta

from celery import shared_task
from django.conf import settings
from django.utils import timezone
from telegram import Bot

from habits.models import Habit

# Инициализация бота
bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)


@shared_task
def send_habit_reminders():
    """Задача Celery для отправки напоминаний пользователям о выполнении привычек.
    - Определяет текущее время и фильтрует привычки, время которых находится в пределах ±5 минут.
    - Для каждой привычки отправляет сообщение в Telegram пользователю, если у него есть chat_id.
    - Ловит и логирует ошибки при отправке сообщений."""

    now = timezone.now()
    start_time = now - timedelta(minutes=5)
    end_time = now + timedelta(minutes=5)

    habits_to_remind = Habit.objects.filter(
        time__gte=start_time.time(), time__lte=end_time.time(), is_public=False
    )

    for habit in habits_to_remind:
        user = habit.user
        chat_id = user.telegram_chat_id
        if chat_id:
            message = f"Напоминание: пора выполнить привычку '{habit.action}'!"

            try:
                bot.send_message(chat_id=chat_id, text=message)
            except Exception as e:
                # Логировать ошибки отправки
                print(f"Ошибка отправки напоминания пользователю {user.email}: {e}")

FROM python:3.12-slim

# Установка необходимых системных пакетов
RUN apt-get update && apt-get install -y \
    gcc build-essential libpq-dev curl \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Создаем пользователя app с домашней директорией /home/app
RUN addgroup --system app && adduser --system --group app --home /home/app

# Создаем рабочие директории и устанавливаем владельца
RUN mkdir -p /home/app /app /app/static && chown -R app:app /home/app /app /app/static

WORKDIR /app

# Переключаемся на пользователя app
USER app

# Обновляем pip и устанавливаем необходимые библиотеки из requirements.txt
ENV PATH="/home/app/.local/bin:$PATH"
COPY --chown=app:app requirements.txt ./

RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Копируем остальной код с нужными правами
COPY --chown=app:app . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

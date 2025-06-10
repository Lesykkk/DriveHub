# Dockerfile

# 1. Базовий образ з Python 3.11
FROM python:3.11-slim

# 2. Встановлюємо робочу директорію всередині контейнера
WORKDIR /app

# 3. Копіюємо тільки файл із залежностями спочатку (для кешування)
COPY requirements.txt .

# 4. Встановлюємо залежності
RUN pip install --upgrade pip && pip install -r requirements.txt

# 5. Копіюємо увесь проєкт у контейнер
COPY . .

# 6. Відкриваємо порт
EXPOSE 8000

# 7. Запускаємо Django-сервер
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

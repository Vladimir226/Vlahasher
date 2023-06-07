# Используем базовый образ с поддержкой GUI
FROM python:3.10-alpine


# Копирование исходного кода приложения

COPY . /app
WORKDIR /app

# Запуск приложения
CMD ["python3", "Vlahasher.py"]



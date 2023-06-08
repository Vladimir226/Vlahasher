# Используем базовый образ
FROM python:3.10-alpine

#Запуск линтера flake8
RUN pip install flake8


# Копирование исходного кода приложения
COPY . /app
WORKDIR /app

# Запуск приложения
CMD ["python3", "Vlahasher.py"]




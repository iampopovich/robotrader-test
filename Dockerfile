FROM python:3.13

WORKDIR /app

# Установка зависимостей
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

# Копирование исходного кода
COPY . .

# Убедимся, что у нас есть все необходимые браузеры
RUN playwright install chromium --with-deps

# Команда по умолчанию
CMD ["pytest", "-v"]

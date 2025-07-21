# robotrader-test

## Что нужно сделать
Написать UI-тест на успешный логин, страница логина - https://stockstrader.roboforex.com/login

## Технические условия
Используй фреймворк pytest-bdd.

## Установка и запуск
1. Установите зависимости:
```bash
pip install -r requirements.txt
```

2. Установите браузеры для Playwright:
```bash
playwright install
```

3. Создайте файл `.env` на основе `.env.example` и заполните необходимые переменные окружения:
```bash
cp .env.example .env
```

4. Запустите тесты:
```bash
pytest -v
```

## Запуск с переменными окружения

### Локально
Можно передать переменные окружения напрямую при запуске:
```bash
TEST_LOGIN_VALID=user@example.com TEST_PASSWORD_VALID=secretpass pytest -v
```

Или использовать параметры pytest для выбора тестов:
```bash
# Запуск конкретного теста по имени
pytest -v -k "test_successful_login"

# Запуск с маркерами
pytest -v -m "login"
```

### Через Docker Compose
Запуск с Docker Compose:
```bash
docker-compose up
```

С переопределением переменных окружения:
```bash
TEST_LOGIN_VALID=user@example.com TEST_PASSWORD_VALID=secretpass docker-compose up
```

Для запуска в режиме без браузерного интерфейса (headless):
```bash
docker-compose up
```
Для запуска с графическим интерфейсом (headed) внутри контейнера, используется xvfb (X Virtual Framebuffer).

Также можно создать файл `.env` в корне проекта, Docker Compose автоматически загрузит переменные из него.

## Полезные ссылки
https://pytest-bdd.readthedocs.io/en/stable/
https://playwright.dev/python/docs/intro

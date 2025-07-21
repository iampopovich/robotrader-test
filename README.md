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

## Полезные ссылки
https://pytest-bdd.readthedocs.io/en/stable/
https://playwright.dev/python/docs/intro

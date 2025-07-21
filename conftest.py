import pytest
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()


@pytest.fixture(scope="session")
def browser():
    """Create a browser instance for the session"""
    import os

    # Определяем, запущены ли мы в Docker контейнере
    in_docker = os.environ.get("IN_DOCKER", "false").lower() == "false"

    # Используем headless=True в Docker, чтобы избежать проблем с X server
    with sync_playwright() as p:
        browser_instance = p.chromium.launch(headless=in_docker)
        yield browser_instance
        browser_instance.close()


@pytest.fixture(scope="function")
def context(browser):
    """Create a new browser context for each test"""
    context_instance = browser.new_context()
    yield context_instance
    context_instance.close()


@pytest.fixture(scope="function")
def page(context):
    """Create a new page for each test"""
    page_instance = context.new_page()
    yield page_instance
    page_instance.close()
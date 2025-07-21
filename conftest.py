import pytest
from playwright.sync_api import sync_playwright


@pytest.fixture(scope="session")
def browser():
    """Create a browser instance for the session"""
    with sync_playwright() as p:
        browser_instance = p.chromium.launch(headless=False)
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
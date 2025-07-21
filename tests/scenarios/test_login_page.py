from pytest_bdd import scenario, given, when, then
from playwright.sync_api import Page, expect
from src.pages.login import LoginPage
import os
import pytest
from dotenv import load_dotenv
import pathlib

# Загружаем переменные окружения из .env файла
load_dotenv()

# Проверяем наличие необходимых переменных окружения
required_env_vars = ["TEST_LOGIN_VALID", "TEST_PASSWORD_VALID"]
missing_vars = [var for var in required_env_vars if os.getenv(var) is None]
if missing_vars:
    print(
        f"WARNING: Следующие переменные окружения не установлены: {', '.join(missing_vars)}"
    )
    print("Используйте файл .env.example как шаблон для создания .env файла")

# Get the absolute path to the feature file
feature_file_path = str(pathlib.Path(__file__).parent.parent / "features" / "login_into_platform.feature")

# Scenarios
@scenario(feature_file_path, "Successful login")
def test_successful_login():
    """User can log in with valid credentials"""


# Given steps
@given("I'm a user")
def im_a_user():
    """User context is established"""


@given("I have an account")
def i_have_an_account():
    """User has a valid account"""


# When steps
@when("I go to the login page")
def i_go_to_login_page(page: Page):
    """Navigate to the login page"""
    login_page = LoginPage(page)
    login_page.navigate("https://stockstrader.roboforex.com/login")
    login_page.handle_cookies_modal(accept_cookies=True)


@when("I fill in the login form with valid credentials")
def i_fill_valid_credentials(page: Page):
    """Fill in the login form with valid credentials"""
    login_page = LoginPage(page)
    # Wait for form elements to be visible
    page.locator(login_page.username_field).wait_for(state="visible", timeout=10000)
    page.locator(login_page.password_field).wait_for(state="visible", timeout=10000)

    # Используем значения из .env файла
    test_login = os.getenv("TEST_LOGIN_VALID")
    test_password = os.getenv("TEST_PASSWORD_VALID")

    # Проверяем, что переменные окружения установлены
    if not test_login or not test_password:
        pytest.skip(
            "Переменные окружения TEST_LOGIN_VALID или TEST_PASSWORD_VALID не установлены"
        )

    login_page.fill(login_page.username_field, test_login)
    login_page.fill(login_page.password_field, test_password)


@when("I fill in the login form with invalid credentials")
def i_fill_invalid_credentials(page: Page):
    """Fill in the login form with invalid credentials"""
    login_page = LoginPage(page)
    # Wait for form elements to be visible
    page.locator(login_page.username_field).wait_for(state="visible", timeout=10000)
    page.locator(login_page.password_field).wait_for(state="visible", timeout=10000)

    login_page.fill(login_page.username_field, "invalid@example.com")
    login_page.fill(login_page.password_field, "wrongpassword")


@when("I fill in the login form with empty credentials")
def i_fill_empty_credentials(page: Page):
    """Fill in the login form with empty credentials"""
    login_page = LoginPage(page)
    # Wait for form elements to be visible
    page.locator(login_page.username_field).wait_for(state="visible", timeout=10000)
    page.locator(login_page.password_field).wait_for(state="visible", timeout=10000)

    login_page.fill(login_page.username_field, "")
    login_page.fill(login_page.password_field, "")


@when("I fill in the login form with credentials for an account that does not exist")
def i_fill_nonexistent_credentials(page: Page):
    """Fill in the login form with credentials for non-existent account"""
    login_page = LoginPage(page)
    # Wait for form elements to be visible
    page.locator(login_page.username_field).wait_for(state="visible", timeout=10000)
    page.locator(login_page.password_field).wait_for(state="visible", timeout=10000)

    login_page.fill(login_page.username_field, "nonexistent@example.com")
    login_page.fill(login_page.password_field, "somepassword")


@when("I press the login button")
def i_press_login_button(page: Page):
    """Click the login button"""
    login_page = LoginPage(page)
    login_page.click(login_page.login_button)


@when("I complete the verification form if it appears")
def i_complete_verification_form(page: Page):
    """Handle the verification form if it appears after login"""
    login_page = LoginPage(page)

    # Wait for possible verification form to appear (up to 10 seconds)
    page.wait_for_timeout(10000)

    # Получаем данные для верификации из .env файла
    phone_digits = os.getenv("PHONE_VERIFICATION")
    birthday_str = os.getenv("DATE_OF_BIRTH")

    # Проверяем, что переменные окружения установлены
    if not phone_digits:
        print(
            "WARNING: Переменная окружения PHONE_VERIFICATION не установлена, используется значение по умолчанию"
        )
        phone_digits = "1234"

    # Если формат даты в .env файле yyyy-mm-dd, преобразуем его в объект datetime
    import datetime

    birth_date = None
    if birthday_str:
        try:
            parts = birthday_str.split("-")
            if len(parts) == 3:
                year, month, day = map(int, parts)
                birth_date = datetime.date(year, month, day)
        except (ValueError, TypeError):
            print(
                f"WARNING: Неверный формат даты рождения: {birthday_str}, используется значение по умолчанию"
            )

    # Если не удалось получить дату из .env или формат неверный, используем значение по умолчанию
    if not birth_date:
        birth_date = datetime.date(1993, 4, 14)  # Значение по умолчанию

    # Обрабатываем форму верификации
    try:
        login_page.handle_verification(
            phone_last_digits=phone_digits, birth_date=birth_date
        )
    except Exception:
        pass


# Then steps
@then("I should be logged in")
def i_should_be_logged_in(page: Page):
    """Verify successful login"""
    # Ждем перенаправления на основную платформу или дашборд
    # Это может занять некоторое время после процесса верификации
    try:
        # Проверяем URL с таймаутом
        expect(page).to_have_url("https://stockstrader.roboforex.com/", timeout=20000)
    except Exception:
        # Если URL не совпадает точно, проверим хотя бы, что мы на главной платформе
        # Это обеспечивает более гибкую проверку, если URL имеет параметры или фрагменты
        current_url = page.url
        assert (
            "stockstrader.roboforex.com" in current_url
        ), f"URL не содержит базовый URL платформы. Текущий URL: {current_url}"
        assert (
            "/login" not in current_url
        ), f"URL все еще содержит путь логина. Текущий URL: {current_url}"

    # Дополнительная проверка: убеждаемся, что страница содержит элементы дашборда
    dashboard_elements = [
        "app-dashboard",  # Предполагаемый корневой компонент дашборда
        "ion-menu",  # Типичный элемент навигации на дашборде
        "[class*='platform-content']",  # Типичный класс для контента после логина
    ]

    # Проверяем наличие хотя бы одного из элементов дашборда
    found_dashboard_element = False
    for selector in dashboard_elements:
        if page.locator(selector).count() > 0:
            found_dashboard_element = True
            break

    assert (
        found_dashboard_element
    ), "Не найдены элементы дашборда на странице после логина"


@then("Dashboard should be displayed")
def dashboard_should_be_displayed(page: Page):
    """Verify that the dashboard is displayed after login"""
    # Ждем, что URL изменится на основной платформы
    expect(page).to_have_url(
        "https://stockstrader.roboforex.com/trading", timeout=20000
    )


@then("I should see an error message indicating invalid credentials")
def i_should_see_invalid_credentials_error(page: Page):
    """Verify invalid credentials error message is displayed"""
    login_page = LoginPage(page)
    error_element = page.locator(login_page.error_message)
    expect(error_element).to_be_visible(timeout=10000)
    # Additional check for specific error text if needed
    # expect(error_element).to_contain_text("Invalid credentials")


@then("I should see an error message indicating that credentials cannot be empty")
def i_should_see_empty_credentials_error(page: Page):
    """Verify empty credentials error message is displayed"""
    login_page = LoginPage(page)
    error_element = page.locator(login_page.error_message)
    expect(error_element).to_be_visible(timeout=10000)
    # Additional check for specific error text if needed
    # expect(error_element).to_contain_text("cannot be empty")


@then("I should see an error message indicating that the account does not exist")
def i_should_see_account_not_exist_error(page: Page):
    """Verify account does not exist error message is displayed"""
    login_page = LoginPage(page)
    error_element = page.locator(login_page.error_message)
    expect(error_element).to_be_visible(timeout=10000)
    # Additional check for specific error text if needed
    # expect(error_element).to_contain_text("account does not exist")

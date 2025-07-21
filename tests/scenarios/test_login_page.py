
from pytest_bdd import scenario, given, when, then
from playwright.sync_api import Page, expect
from src.pages.login import LoginPage
import os


# Scenarios
@scenario('../features/login_into_platform.feature', 'Successful login')
def test_successful_login():
    """User can log in with valid credentials"""


@scenario('../features/login_into_platform.feature', 'Unsuccessful login')
def test_unsuccessful_login():
    """User cannot log in with invalid credentials"""


@scenario('../features/login_into_platform.feature', 'Login with empty credentials')
def test_login_with_empty_credentials():
    """User cannot log in with empty credentials"""


@scenario('../features/login_into_platform.feature', 'Login with unexisting account')
def test_login_with_unexisting_account():
    """User cannot log in with unexisting account"""


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
    page.goto("https://stockstrader.roboforex.com/login")
    # Wait for page to load completely
    page.wait_for_load_state("domcontentloaded", timeout=30000)

    # Additional wait for Angular/Ionic app to initialize
    page.wait_for_timeout(3000)

    # Check if cookies modal is visible and handle it
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

    # Using test credentials - in real tests these should come from config/env
    login_page.fill(login_page.username_field, os.getenv("TEST_LOGIN_VALID"))
    login_page.fill(login_page.password_field, os.getenv("TEST_PASSWORD_VALID"))


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
    # Debug: take a screenshot to see current page state
    page.click(LoginPage.login_button)


# Then steps
@then("I should be logged in")
def i_should_be_logged_in(page: Page):
    """Verify successful login"""
    # Wait for redirect to main platform or dashboard
    # This selector should be updated based on actual post-login page structure
    expect(page).to_have_url("https://stockstrader.roboforex.com/", timeout=10000)


@then("I should see an error message indicating invalid credentials")
def i_should_see_invalid_credentials_error(page: Page):
    """Verify invalid credentials error message is displayed"""
    login_page = LoginPage(page)
    error_element = page.locator(login_page.error_message)
    expect(error_element).to_be_visible(timeout=5000)
    # Additional check for specific error text if needed
    # expect(error_element).to_contain_text("Invalid credentials")


@then("I should see an error message indicating that credentials cannot be empty")
def i_should_see_empty_credentials_error(page: Page):
    """Verify empty credentials error message is displayed"""
    login_page = LoginPage(page)
    error_element = page.locator(login_page.error_message)
    expect(error_element).to_be_visible(timeout=5000)
    # Additional check for specific error text if needed
    # expect(error_element).to_contain_text("cannot be empty")


@then("I should see an error message indicating that the account does not exist")
def i_should_see_account_not_exist_error(page: Page):
    """Verify account does not exist error message is displayed"""
    login_page = LoginPage(page)
    error_element = page.locator(login_page.error_message)
    expect(error_element).to_be_visible(timeout=5000)
    # Additional check for specific error text if needed
    # expect(error_element).to_contain_text("account does not exist")




from pytest_bdd import scenario, given, when, then

@scenario('login_page.feature', 'User can log in with valid credentials')
def test_user_can_log_in_with_valid_credentials():
    """User can log in with valid credentials"""

    pass

@scenario('login_page.feature', 'User cannot log in with invalid credentials')
def test_user_cannot_log_in_with_invalid_credentials():
    """User cannot log in with invalid credentials"""

    pass



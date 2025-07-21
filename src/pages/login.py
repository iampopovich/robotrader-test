from src.pages.base_page import BasePage


class LoginPage(BasePage):
    username_field = "ion-input#email input"
    password_field = "ion-input#password input"
    login_button = 'ion-button[color="primary"]'
    error_message = ".error-message, .alert, [class*='error']"

    def login(self, username, password):
        self.fill(self.username_field, username)
        self.fill(self.password_field, password)
        self.click(self.login_button)

    def get_error_message(self):
        return self.get_text(self.error_message)

from src.pages.base_page import BasePage


class LoginPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.username_field = "ion-input#email"
        self.password_field = "ion-input#password"
        self.login_button = 'ion-button[translate="login.Continue"]'
        self.error_message = ".error-message, .alert, [class*='error']"

    def login(self, username, password):
        self.fill(self.username_field, username)
        self.fill(self.password_field, password)
        self.click(self.login_button)

    async def login_with_cookies_handling(self, username, password, accept_cookies=True):
        """Логин с автоматической обработкой куки модального окна"""
        if accept_cookies:
            await self.accept_cookies()
        else:
            await self.decline_cookies()

        self.fill(self.username_field, username)
        self.fill(self.password_field, password)
        self.click(self.login_button)

    def get_error_message(self):
        return self.get_text(self.error_message)

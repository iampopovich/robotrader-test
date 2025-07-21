class LoginPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.username_field = "input type email"
        self.password_field = "input type password"
        self.login_button = "ion button"

    def login(self, username, password):
        self.fill(self.username_field, username)
        self.fill(self.password_field, password)
        self.click(self.login_button)

    def get_error_message(self):
        return self.get_text(self.error_message)

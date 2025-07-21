class BasePage:
    def __init__(self, page):
        self.page = page

    def navigate(self, url):
        self.page.goto(url)

    def wait_for_response(self, url):
        self.page.wait_for_response(url)

    def click(self, selector):
        self.page.click(selector)

    def fill(self, selector, text):
        self.page.fill(selector, text)

    def get_text(self, selector):
        return self.page.text_content(selector)

    def accept_cookies(self):
        try:
            self.page.click('button:has-text("Accept")')
        except Exception as e:
            print(f"Error accepting cookies: {e}")

    def decline_cookies(self):
        try:
            self.page.click('button:has-text("Decline")')
        except Exception as e:
            print(f"Error declining cookies: {e}")

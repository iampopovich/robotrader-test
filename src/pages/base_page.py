class BasePage:

    cookies_modal = 'ion-modal.cookie, rg-cookie, [class*="cookies"], [class*="cookie-banner"]'
    cookies_allow_button = 'ion-button[translate="cookies.allow"]'
    cookies_decline_button = 'ion-button[translate="cookies.disallow"]'


    def __init__(self, page):
        self.page = page

    def handle_cookies_modal(self, accept_cookies=True, timeout=10000):
        """Синхронный метод для обработки модального окна с куки"""
        try:
            # Проверяем, есть ли модальное окно с куки на странице
            cookies_modal = self.page.wait_for_selector(self.cookies_modal, timeout=timeout)
            if cookies_modal.is_visible():
                if accept_cookies:
                    # Нажимаем кнопку принятия куки
                    accept_button = self.page.wait_for_selector(self.cookies_allow_button, timeout=2000)
                    if accept_button.is_visible():
                        accept_button.click()
                        return True
                else:
                    # Нажимаем кнопку отклонения куки
                    decline_button = self.page.wait_for_selector(self.cookies_decline_button, timeout=2000)
                    if decline_button.is_visible():
                        decline_button.click()
                        return True
            return False
        except (TimeoutError, RuntimeError) as e:
            # Если модальное окно не появляется или происходит ошибка, продолжаем
            print(f"Cookie modal handling failed: {e}")
            return False

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

    async def wait_for_cookies_modal_appears(self, timeout=5000):
        """Асинхронно ожидает появления модального окна с куки"""
        try:
            await self.page.wait_for_selector(self.cookies_modal, timeout=timeout)
            return True
        except TimeoutError:
            return False

    async def wait_for_cookies_modal_not_appears(self, timeout=5000):
        """Асинхронно ожидает исчезновения модального окна с куки"""
        try:
            await self.page.wait_for_selector(self.cookies_modal, state='hidden', timeout=timeout)
            return True
        except TimeoutError:
            return False

class BasePage:

    cookies_modal = 'ion-modal.cookie, rg-cookie, [class*="cookies"], [class*="cookie-banner"]'
    cookies_allow_button = 'ion-button[translate="cookies.allow"]'
    cookies_decline_button = 'ion-button[translate="cookies.disallow"]'


    def __init__(self, page):
        self.page = page

    def navigate(self, url):
        self.page.goto(url)

    async def navigate_and_handle_cookies(self, url, accept_cookies=True):
        """Навигация на страницу с автоматической обработкой куки"""
        self.page.goto(url)
        if accept_cookies:
            await self.accept_cookies()
        else:
            await self.decline_cookies()

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

    async def accept_cookies(self):
        """Принимает куки, если модальное окно присутствует"""
        try:
            if await self.wait_for_cookies_modal_appears(timeout=3000):
                await self.page.click(self.cookies_allow_button)
                await self.wait_for_cookies_modal_not_appears()
                return True
            return False
        except (TimeoutError, RuntimeError) as e:
            print(f"Error accepting cookies: {e}")
            return False

    async def decline_cookies(self):
        """Отклоняет куки, если модальное окно присутствует"""
        try:
            if await self.wait_for_cookies_modal_appears(timeout=3000):
                await self.page.click(self.cookies_decline_button)
                await self.wait_for_cookies_modal_not_appears()
                return True
            return False
        except (TimeoutError, RuntimeError) as e:
            print(f"Error declining cookies: {e}")
            return False

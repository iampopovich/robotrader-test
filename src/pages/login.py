from src.pages.base_page import BasePage
import datetime


class LoginPage(BasePage):
    username_field = "ion-input#email input"
    password_field = "ion-input#password input"
    login_button = 'ion-button[color="primary"]'
    error_message = ".error-message, .alert, [class*='error']"

    # Селекторы для формы верификации
    verification_form = 'rg-equipment-two-step-portal, form[class*="ng-invalid"]'
    verification_header = 'ion-label[translate="verification.two-step.equipment.header"]'
    phone_input = 'ion-input[formcontrolname="phone"] input, input#ion-input-2'
    date_picker_trigger = '#calendar-trigger'
    birthday_input = 'ion-input[formcontrolname="birthday"]'
    date_picker_popup = 'ion-popover'
    date_picker_day = 'button.calendar-day'  # Селектор для дня в календаре
    date_picker_month = 'ion-segment-button.calendar-month'  # Селектор для выбора месяца
    date_picker_year = 'ion-segment-button.calendar-year'  # Селектор для выбора года
    submit_verification_button = 'ion-button[type="submit"]'

    def login(self, username, password):
        self.fill(self.username_field, username)
        self.fill(self.password_field, password)
        self.click(self.login_button)

    def get_error_message(self):
        return self.get_text(self.error_message)

    def handle_verification(self, phone_last_digits="1234", birth_date=datetime.date(1993, 4, 14)):
        """Обрабатывает форму верификации, если она появляется после входа

        Args:
            phone_last_digits (str): Последние 4 цифры номера телефона
            birth_date (datetime.date): Дата рождения в формате datetime.date

        Returns:
            bool: True если форма была обработана, False если форма не появилась
        """
        try:
            # Проверяем, появилась ли форма верификации
            verification_form = self.page.wait_for_selector(self.verification_form, timeout=10000)
            if verification_form.is_visible():
                print("Верификационная форма обнаружена")

                # Заполняем последние 4 цифры номера телефона
                phone_field = self.page.wait_for_selector(self.phone_input, timeout=10000)
                if phone_field.is_visible():
                    phone_field.fill(phone_last_digits)

                # Открываем выбор даты
                date_trigger = self.page.wait_for_selector(self.date_picker_trigger, timeout=10000)
                if date_trigger.is_visible():
                    date_trigger.click()

                    # Ждем появления календаря
                    self.page.wait_for_timeout(5000)

                    self.page.get_by_role("button", name="Choose month and year").click()
                    self.page.get_by_role("button", name="Previous 24 years").click()
                    self.page.get_by_role("button", name="1993").click()
                    self.page.get_by_role("button", name="April").click()
                    self.page.locator("button").filter(has_text="14").click()
                    self.page.get_by_role("button", name="Set").click()
                    self.page.get_by_role("button", name="Confirm").click()

                # Нажимаем кнопку подтверждения
                submit_button = self.page.wait_for_selector(self.submit_verification_button, timeout=10000)
                if submit_button.is_visible():
                    submit_button.click()
                return True

            return False
        except (TimeoutError, RuntimeError) as e:
            print(f"Ошибка при обработке формы верификации: {e}")
            return False

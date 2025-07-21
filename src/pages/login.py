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
            verification_form = self.page.wait_for_selector(self.verification_form, timeout=5000)
            if verification_form.is_visible():
                print("Верификационная форма обнаружена")

                # Заполняем последние 4 цифры номера телефона
                phone_field = self.page.wait_for_selector(self.phone_input, timeout=2000)
                if phone_field.is_visible():
                    phone_field.fill(phone_last_digits)

                # Открываем выбор даты
                date_trigger = self.page.wait_for_selector(self.date_picker_trigger, timeout=2000)
                if date_trigger.is_visible():
                    date_trigger.click()

                    # Ждем появления календаря
                    self.page.wait_for_timeout(1000)

                    # Выбираем год (1993)
                    year_buttons = self.page.locator(self.date_picker_year)
                    for i in range(year_buttons.count()):
                        year_text = year_buttons.nth(i).text_content()
                        if year_text and str(birth_date.year) in year_text:
                            year_buttons.nth(i).click()
                            break

                    # Выбираем месяц (апрель - 4)
                    month_buttons = self.page.locator(self.date_picker_month)
                    for i in range(month_buttons.count()):
                        month_button = month_buttons.nth(i)
                        # Апрель должен быть 4-м месяцем (0-индексированный массив)
                        if i == birth_date.month - 1:
                            month_button.click()
                            break

                    # Выбираем день (14)
                    day_buttons = self.page.locator(self.date_picker_day)
                    for i in range(day_buttons.count()):
                        day_text = day_buttons.nth(i).text_content()
                        if day_text and day_text.strip() == str(birth_date.day):
                            day_buttons.nth(i).click()
                            break

                # Нажимаем кнопку подтверждения
                submit_button = self.page.wait_for_selector(self.submit_verification_button, timeout=2000)
                if submit_button.is_visible():
                    submit_button.click()
                return True

            return False
        except (TimeoutError, RuntimeError) as e:
            print(f"Ошибка при обработке формы верификации: {e}")
            return False

from framework.pages.base_page import BasePage
from selenium.webdriver.common.by import By
from framework.elements.text_box import TextBox
from framework.elements.button import Button


class YandexSignInPage(BasePage):
    search_condition = By.XPATH

    headline_locator = "//div[@class='Header']"
    login_text_field = "//input[@name='login']"
    password_text_field = "//input[@name='passwd']"
    sign_in_button = "//button[contains(@id, 'sign-in')]"

    def __init__(self) -> None:
        super().__init__(search_condition=YandexSignInPage.search_condition,
                         locator=YandexSignInPage.headline_locator,
                         page_name=self.__class__.__name__)

    def fill_in_the_login_text_filed(self, login: str) -> None:
        login_text_field = TextBox(self.search_condition, self.login_text_field, "login_text_field")
        login_text_field.send_text(login)

    def fill_in_the_password_text_filed(self, login: str) -> None:
        password_text_field = TextBox(self.search_condition, self.password_text_field, "password_text_field")
        password_text_field.send_text(login)

    def click_sign_in_button(self) -> None:
        sign_in_button = Button(self.search_condition, self.sign_in_button, "sign_in_button")
        sign_in_button.click()

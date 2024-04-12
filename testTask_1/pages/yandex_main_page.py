from framework.pages.base_page import BasePage
from selenium.webdriver.common.by import By
from framework.elements.button import Button
from framework.elements.label import Label


class YandexMainPage(BasePage):
    search_condition = By.XPATH

    headline_locator = "//div[@class='headline']"
    login_button_locator = "//a[contains(@class, 'personal-enter')]"
    user_avatar_label = "//div[@class='usermenu-portal']"
    user_disk_menu_item = "//a[contains(@class, 'MenuItem_disk')]"
    user_menu_iframe = "//iframe[contains(@class, 'usermenu')]"

    def __init__(self) -> None:
        super().__init__(search_condition=YandexMainPage.search_condition,
                         locator=YandexMainPage.headline_locator,
                         page_name=self.__class__.__name__)

    def go_to_login_page(self) -> None:
        login_button = Button(self.search_condition, self.login_button_locator, "login_button")
        login_button.click()

    def is_user_avatar_label_displayed(self) -> bool:
        user_avatar_image = Label(self.search_condition, self.user_avatar_label, "user_avatar_label")
        return user_avatar_image.is_displayed()

    def go_to_user_disk_page(self) -> None:
        user_disk_menu_item = Button(self.search_condition, self.user_disk_menu_item, "user_disk_menu_item")
        user_avatar_image = Label(self.search_condition, self.user_avatar_label, "user_avatar_label")
        user_avatar_image.click()
        self.wait_iframe_and_switch_on_it(self.user_menu_iframe)
        user_disk_menu_item.click()


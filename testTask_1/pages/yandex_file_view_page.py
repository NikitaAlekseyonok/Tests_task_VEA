from framework.pages.base_page import BasePage
from selenium.webdriver.common.by import By
from framework.elements.label import Label


class YandexFileViewPage(BasePage):
    search_condition = By.XPATH

    headline_locator = "//div[@class='headline']"
    file_name_label = "//h2[text()='{file_name}']"

    def __init__(self) -> None:
        super().__init__(search_condition=YandexFileViewPage.search_condition,
                         locator=YandexFileViewPage.headline_locator,
                         page_name=self.__class__.__name__)

    def is_file_name_displayed(self, file_name: str) -> bool:
        file_name_label = Label(self.search_condition, self.file_name_label.format(file_name), "file_name_label")

        return file_name_label.is_displayed()

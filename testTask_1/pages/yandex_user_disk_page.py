from framework.pages.base_page import BasePage
from selenium.webdriver.common.by import By
from framework.elements.text_box import TextBox
from framework.elements.button import Button
from framework.elements.label import Label


class YandexUserDiskPage(BasePage):
    search_condition = By.XPATH

    yandex_logo = "//div[contains(@class, 'PSHeaderLogo360')]"
    create_resource_button = "//span[contains(@class, 'create')]//button"
    create_folder_resource_button = "//button[contains(@class, 'create-resource') and @aria-label='Папку']"
    crete_folder_dialog_window = "//div[contains(@class, 'dialog')]"
    folder_name_text_field = "//form[contains(@class, 'rename')]//input"
    submit_button = "//button[contains(@class, 'submit')]"
    item_by_name = "//div[contains(@class, 'listing-item')]//span[text()='{item_name}']"
    input_file_filed = "//div[contains(@class, 'upload')]//input[@type='file']"

    def __init__(self) -> None:
        super().__init__(search_condition=YandexUserDiskPage.search_condition,
                         locator=YandexUserDiskPage.yandex_logo,
                         page_name=self.__class__.__name__)

    def create_new_folder(self, folder_name: str) -> bool:
        create_resource_button = Button(self.search_condition, self.create_resource_button, "create_resource_button")
        create_folder_resource_button = Button(self.search_condition, self.create_folder_resource_button,
                                               "create_folder_resource_button")
        folder_name_text_field = TextBox(self.search_condition, self.folder_name_text_field, "folder_name_text_field")
        submit_button = Button(self.search_condition, self.submit_button, "submit_button")

        create_resource_button.click()
        create_folder_resource_button.click()

        if not self.is_dialog_window_displayed():
            return False

        folder_name_text_field.clear_field()
        folder_name_text_field.send_text(folder_name)
        submit_button.click()

        return True

    def is_dialog_window_displayed(self) -> bool:
        crete_folder_dialog_window = Label(self.search_condition, self.crete_folder_dialog_window,
                                           "crete_folder_dialog_window")

        return crete_folder_dialog_window.is_displayed()

    def is_item_with_name_exist(self, item_name: str) -> bool:
        item_label = Label(self.search_condition, self.item_by_name.format(item_name=item_name), "item_label")

        return item_label.is_displayed()

    def open_item_by_name(self, item_name: str) -> None:
        item_label = Label(self.search_condition, self.item_by_name.format(item_name=item_name), "item_label")

        item_label.double_click()

    def create_new_file(self, file_path: str) -> None:
        input_file_filed = TextBox(self.search_condition, self.input_file_filed, "input_file_filed")

        input_file_filed.send_keys(file_path)


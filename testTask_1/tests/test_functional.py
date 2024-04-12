import os
from framework.utils import string_util
from config.test_data import FILE_NAME_FOR_TEST
from config.creds import Creds
from config.urls import Urls
from pages.yandex_main_page import YandexMainPage
from pages.yandex_signIn_page import YandexSignInPage
from pages.yandex_user_disk_page import YandexUserDiskPage
from pages.yandex_file_view_page import YandexFileViewPage


class TestYandexFileStorge:

    TEST_FILE_PATH = os.path.abspath(f"config/{FILE_NAME_FOR_TEST}")

    def test_yandex_file_storage(self, create_browser):
        browser = create_browser

        yandex_main_page = YandexMainPage()
        browser.set_url(Urls.YANDEX_MAIN_PAGE_URL)
        assert yandex_main_page.is_opened(), "The main yandex page is not open"

        yandex_main_page.go_to_login_page()
        yandex_sign_in_page = YandexSignInPage()
        assert yandex_sign_in_page.is_opened(), "The sign-in yandex page is not open"

        yandex_sign_in_page.fill_in_the_login_text_filed(Creds.login)
        yandex_sign_in_page.click_sign_in_button()
        yandex_sign_in_page.fill_in_the_password_text_filed(Creds.password)
        yandex_sign_in_page.click_sign_in_button()
        assert yandex_main_page.is_opened(),  "The main yandex page is not open"
        assert yandex_main_page.is_user_avatar_label_displayed(),  "The user avatar is not displayed on the page"

        yandex_main_page.go_to_user_disk_page()
        yandex_user_disk_page = YandexUserDiskPage()
        browser.switch_to_window()
        yandex_main_page.switch_to_default_content()
        browser.switch_new_window()
        assert yandex_user_disk_page.is_opened(),  "The user disk yandex page is not open"

        new_folder_name = string_util.set_random_string()
        assert yandex_user_disk_page.create_new_folder(new_folder_name), "The was a problem creating the folder"

        yandex_user_disk_page.refresh_page()
        assert yandex_user_disk_page.is_item_with_name_exist(new_folder_name), "The folder with name  does not exist"

        yandex_user_disk_page.open_item_by_name(new_folder_name)
        yandex_user_disk_page.create_new_file(self.TEST_FILE_PATH)
        assert yandex_user_disk_page.is_item_with_name_exist(FILE_NAME_FOR_TEST), \
            f"The file with name {FILE_NAME_FOR_TEST}has not been created"

        yandex_user_disk_page.open_item_by_name(FILE_NAME_FOR_TEST)
        yandex_file_view_page = YandexFileViewPage()
        assert yandex_file_view_page.is_opened(), "The file view yandex page is not open"
        assert yandex_file_view_page.is_file_name_displayed(FILE_NAME_FOR_TEST),\
            f"The file name {FILE_NAME_FOR_TEST} is not displayed"



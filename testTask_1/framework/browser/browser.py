from selenium.common.exceptions import NoSuchWindowException, TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from config.waits import Waits
from config.browser import BrowserConfig
from .browser_factory import BrowserFactory
from framework.utils.logger_helper import Logger
from framework.waits.wait_for_ready_state_complete import WaitForReadyStateComplete
from framework.singleton import Singleton


class Browser(metaclass=Singleton):
    def __init__(self):
        self.__web_driver = {}
        self.__main_window_handle = None
        self.__selected_browser = BrowserConfig.BROWSER

    @staticmethod
    def get_browser():
        return Browser()

    def get_selected_browser_key(self):
        return self.__selected_browser

    def get_browser_keys(self):
        return self.__web_driver.keys()

    def get_driver_names(self):
        return self.__web_driver.keys()

    def get_driver(self):
        return self.__web_driver[self.__selected_browser]

    def set_up_driver(self, browser_key=BrowserConfig.BROWSER, is_incognito=False,
                      enable_performance_logging=False):
        Logger.info('Инициализация драйвера для браузера ' + BrowserConfig.BROWSER)
        if browser_key in self.__web_driver:
            raise ValueError("Браузер с  ключом '{}', уже создан.".format(browser_key))
        self.__web_driver[browser_key] = \
            BrowserFactory.get_browser_driver(is_incognito=is_incognito,
                                              enable_performance_logging=enable_performance_logging)
        self.__web_driver[browser_key].set_page_load_timeout(Waits.PAGE_LOAD_TIMEOUT_SEC)
        self.__web_driver[browser_key].set_script_timeout(Waits.SCRIPT_TIMEOUT_SEC)
        self.__main_window_handle = self.__web_driver[browser_key].current_window_handle
        self.select_browser(browser_key)

    def select_browser(self, browser_key=BrowserConfig.BROWSER):
        if browser_key not in self.__web_driver:
            raise KeyError("Браузер с  ключом '{}', не существует.".format(browser_key))
        self.__selected_browser = browser_key

    def quit(self, browser_key=BrowserConfig.BROWSER):
        browser_inst = self.__web_driver.get(browser_key)
        if browser_inst is not None:
            browser_inst.quit()
            self.__web_driver.pop(browser_key, None)

    def close(self, page_name=""):
        if self.get_driver() is not None:
            Logger.info("Закрытие страницы %s " % page_name)
            self.get_driver().close()

    def refresh_page(self):
        Logger.info("Перезагрузка страницы")
        self.get_driver().refresh()

    def maximize(self, browser_key=BrowserConfig.BROWSER):
        self.__web_driver[browser_key].maximize_window()

    def set_url(self, url):
        Logger.info("Изменение url страницы на " + url)
        self.get_driver().get(url)

    def get_current_url(self):
        return self.get_driver().current_url

    def back_page(self):
        self.get_driver().back()

    def switch_to_window(self, window_handle=None):
        if window_handle is None:
            window_handle = self.__main_window_handle
        Logger.info("Переключение на окно с именем %s" % window_handle)
        try:
            self.get_driver().switch_to.window(window_handle)
        except NoSuchWindowException:
            Logger.error("Не найдено подходящее окно с менем %s" % window_handle)
            return False

    def switch_new_window(self, logged_page_name=""):
        Logger.info("Переключение на новое окно %s" % logged_page_name)
        handles = self.get_driver().window_handles
        if len(handles) <= 1:
            raise NoSuchWindowException("Нет нового окна. Количество окон равно %s" % len(handles))
        self.get_driver().switch_to.window(handles[-1])

    def wait_for_page_to_load(self):
        WebDriverWait(self.get_driver(), Waits.PAGE_LOAD_TIMEOUT_SEC).until(WaitForReadyStateComplete(browser=self))

    def is_wait_successful(self, wait_function, *args):
        try:
            wait_function(*args)
        except TimeoutException:
            return False
        return True

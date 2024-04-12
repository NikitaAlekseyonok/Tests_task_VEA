from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from framework.utils.logger_helper import Logger
from framework.browser.browser import Browser
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from config.waits import Waits


class BaseElement:
    coordinate_x = 'x'
    coordinate_y = 'y'

    # @abstractmethod
    def __init__(self, search_condition_of, loc, name_of):
        self.__search_condition = search_condition_of
        self.__locator = loc
        self.__name = name_of

    def __getitem__(self, key):
        if self.__search_condition != By.XPATH:
            raise TypeError("__getitem__ for BaseElement possible only when __search_condition == By.XPATH")
        else:
            return type(self)(By.XPATH, self.__locator + "[" + str(key) + "]", self.__name)
            # return type(self)(By.XPATH, "(" + self.__locator + ")" + "[" + str(key) + "]", self.__name)

    def __call__(self, sublocator, new_name_of=None):
        if new_name_of is not None:
            return type(self)(By.XPATH, self.__locator + sublocator, new_name_of)
        else:
            return type(self)(By.XPATH, self.__locator + sublocator, self.__name)

    def get_locator(self):
        return self.__locator

    def get_search_condition(self):
        return self.__search_condition

    def find_element(self):
        waiter = ec.presence_of_element_located((self.get_search_condition(), self.get_locator()))
        element = self.wait_for_check_by_condition(method_to_check=waiter, message=" не был найден")
        return element

    def get_elements(self):
        return Browser.get_browser().get_driver().find_elements(self.__search_condition, self.__locator)

    def is_enabled(self):
        return self.find_element().is_enabled()

    def is_disabled(self):
        return self.find_element().is_disabled()

    def get_name(self):
        return self.__name

    def is_displayed(self):
        try:
            if not self.is_exist():
                return False
            return self.find_element().is_displayed()
        except TimeoutException:
            return False

    def is_exist(self):
        return self.get_elements_count() > 0

    def get_elements_count(self):
        elements_count = len(Browser.get_browser().get_driver().find_elements(self.__search_condition, self.__locator))
        return elements_count

    def send_keys(self, key):
        self.click()
        self.send_keys_without_click(key)

    def send_keys_without_click(self, key):
        Logger.info("send_keys: Изменение текста для элемента '" + self.get_name() + " " + self.__class__.__name__ +
                    "'" + "' на текст => '"  + "'")
        self.wait_for_is_visible()
        element = self.wait_for_clickable()
        element.send_keys(key)

    def click(self):
        Logger.info("click: Щелчок по элемету '" + self.get_name() + " " + self.__class__.__name__ + "'")

        def func():
            self.find_element().click()
            return True

        self.wait_for(func)

    def wait_for(self, condition, *args, **kwargs):
        def func(driver):
            try:
                value = condition(*args, **kwargs)
                return value
            except StaleElementReferenceException:
                return False

        return WebDriverWait(Browser.get_browser().get_driver(), Waits.EXPLICITLY_WAIT_SEC,
                             ignored_exceptions=[StaleElementReferenceException]).until(func)

    def js_click(self):
        element = self.wait_for_clickable()
        Browser.get_browser().get_driver().execute_script("arguments[0].click();", element)

    def actions_click(self):
        actions = ActionChains(Browser.get_browser().get_driver())
        actions.click(on_element=self.find_element())
        actions.perform()

    def actions_click_with_key(self, key):
        actions = ActionChains(Browser.get_browser().get_driver())
        actions.key_down(value=key).click(self.find_element()).key_up(value=key).perform()

    def send_keys_to_element(self, keys):
        actions = ActionChains(Browser.get_browser().get_driver())
        actions.send_keys_to_element(self.find_element(), keys)
        actions.perform()

    def get_text(self):
        Logger.info("get_text: Получение текста для элемента '" + self.get_name() + "'")
        self.wait_for_is_present()
        text = self.find_element().text
        Logger.info("get_text: Получен текст '" + text + "'")
        return text

    def get_text_content(self):
        self.wait_for_is_visible()
        return Browser.get_browser().get_driver().\
            execute_script("return arguments[0].textContent;", self.find_element())

    def get_attribute(self, attr):
        Logger.info("get_attribute: Получение атрибута " + attr + " для элемента '" + self.get_name() + "'")
        self.wait_for_is_visible()
        return self.find_element().get_attribute(name=attr)

    def scroll_by_script(self):
        self.wait_for_is_visible()
        Logger.info("Скролл к элементу '" + self.get_name() + "'")
        Browser.get_browser().execute_script("arguments[0].scrollIntoView();", self.find_element())

    def double_click(self):
        self.wait_for_is_visible()
        Logger.info("double_click: Двойной щелчок по элементу '" + self.get_name() + "'")
        ActionChains(Browser.get_browser().get_driver()).double_click(self.find_element()).perform()

    def wait_for_clickable(self):
        waiter = ec.element_to_be_clickable((self.get_search_condition(), self.get_locator()))
        return self.wait_for_check_by_condition(method_to_check=waiter, message=" не доступен для щелчка")

    def wait_for_is_visible(self):
        self.wait_for_is_present()
        waiter = ec.visibility_of_element_located((self.get_search_condition(), self.get_locator()))
        self.wait_for_check_by_condition(method_to_check=waiter, message=" не видим")

    def wait_for_is_present(self):
        waiter = ec.presence_of_element_located((self.get_search_condition(), self.get_locator()))
        self.wait_for_check_by_condition(method_to_check=waiter, message=" не существует")

    def wait_for_is_displayed(self, wait_time):
        Browser.get_browser().wait_for_true(self.is_displayed, wait_time)

    def get_location(self):
        return self.find_element().location

    def get_location_vertical(self):
        return self.find_element().location[BaseElement.coordinate_y]

    def get_location_horizontal(self):
        return self.find_element().location[BaseElement.coordinate_x]

    def wait_for_check_by_condition(self, method_to_check, message,
                                    wait_time_sec=Waits.EXPLICITLY_WAIT_SEC, use_default_msg=True):
        try:
            element = WebDriverWait(Browser.get_browser().get_driver(), wait_time_sec).until(method=method_to_check)
        except TimeoutException:
            result_message = ("элемент '" + self.get_name() + "' с локатором " + self.get_locator() + message
                              if use_default_msg else message)
            Logger.warning(result_message)
            raise TimeoutException(result_message)
        return element


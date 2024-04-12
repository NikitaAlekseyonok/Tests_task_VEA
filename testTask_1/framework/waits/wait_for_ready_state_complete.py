from selenium.common.exceptions import StaleElementReferenceException
from framework.constants import page_states


class WaitForReadyStateComplete(object):
    def __init__(self, browser):
        self.browser = browser

    def __call__(self, driver):
        try:
            return driver.execute_script('return document.readyState') == page_states.COMPLETE
        except StaleElementReferenceException:
            return False

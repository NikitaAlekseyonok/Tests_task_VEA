import pytest
from framework.browser.browser import Browser
from config.browser import BrowserConfig


@pytest.fixture(scope="session")
def create_browser():
    Browser.get_browser().set_up_driver(is_incognito=True)
    Browser.get_browser().maximize(browser_key=BrowserConfig.BROWSER)
    yield Browser.get_browser()

    for browser_key in list(Browser.get_browser().get_driver_names()):
        Browser.get_browser().quit(browser_key=browser_key)

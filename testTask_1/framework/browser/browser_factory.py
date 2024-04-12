from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from config.browser import BrowserConfig
from framework.constants import browsers
from os import environ


class BrowserFactory:

    @staticmethod
    def get_browser_driver(is_incognito=False, enable_performance_logging=False):
        if BrowserConfig.BROWSER == browsers.BROWSER_CHROME:
            chrome_options = webdriver.ChromeOptions()

            if is_incognito:
                chrome_options.add_argument("--incognito")

            service = Service(ChromeDriverManager().install())
            return webdriver.Chrome(service=service, options=chrome_options)

        elif BrowserConfig.BROWSER == browsers.BROWSER_FIREFOX:
            firefox_profile = webdriver.FirefoxProfile()
            firefox_options = None
            if is_incognito:
                firefox_profile.set_preference("browser.privatebrowsing.autostart", True)
            if enable_performance_logging:
                open("perfLog.txt", "w").close()
                environ["MOZ_LOG"] = "timestamp,sync,nsHttp:3"

            return webdriver.Firefox(options=firefox_options)

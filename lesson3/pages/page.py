from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import *


class Page(object):
    def __init__(self, driver, base_url):
        self.driver = driver
        self.base_url = base_url
        self.wait = WebDriverWait(driver, 10)

    def is_element_visible(self, locator):
        try:
            self.wait.until(visibility_of_element_located(locator))
            return True
        except WebDriverException:
            return False
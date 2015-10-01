from page import Page
from selenium.webdriver.common.by import By


class LoginPage(Page):

    @property
    def username_field(self):
        return self.driver.find_element_by_id("username")

    @property
    def password_field(self):
        return self.driver.find_element_by_name("password")

    @property
    def submit_button(self):
        return self.driver.find_element_by_name("submit")

    @property
    def is_this_page(self):
        return self.is_element_visible((By.ID, "loginform"))

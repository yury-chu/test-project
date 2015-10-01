from php4dvd.pages.page import Page
from selenium.webdriver.support.select import Select


class UserForm(Page):

    @property
    def username_field(self):
        return self.driver.find_element_by_name("username")

    @property
    def email_field(self):
        return self.driver.find_element_by_name("email")

    @property
    def password_field(self):
        return self.driver.find_element_by_name("password")

    @property
    def password1_field(self):
        return self.driver.find_element_by_name("password2")

    @property
    def role_select(self):
        return Select(self.driver.find_element_by_name("role"))

    @property
    def submit_button(self):
        return self.driver.find_element_by_name("submit")


from internal_page import InternalPage
from php4dvd.pages.blocks.user_form import UserForm
from selenium.webdriver.support.select import Select


class UserManagementPage(InternalPage):

    def __init__(self, driver, base_url):
        super(UserManagementPage, self).__init__(driver, base_url)
        self.user_form = UserForm(self.driver, self.base_url)

    # more page elements here
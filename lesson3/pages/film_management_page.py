from internal_page import InternalPage
from lesson3.pages.blocks.film_form import FilmForm
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By


class FilmManagementPage(InternalPage):

    def __init__(self, driver):
        super(FilmManagementPage, self).__init__(driver)
        self.user_form = FilmForm(self.driver)

    @property
    def go_to_film_management(self):
        return self.driver.find_element_by_css_selector("img[alt=\"Add movie\"]")

    @property
    def name_field(self):
        return self.driver.find_element_by_name("name")

    @property
    def year_field(self):
        return self.driver.find_element_by_name("year")

    @property
    def frmt_field(self):
        return self.driver.find_element_by_name("format")

    @property
    def note_feild(self):
        return self.driver.find_element_by_name("notes")

    @property
    def button_save(self):
        return self.driver.find_element_by_name("submit")

    @property
    def is_this_page(self):
        return self.is_element_visible((By.XPATH, "//img[@title='Save']"))

    @property
    def link_to_main_page(self):
        return self.driver.find_element_by_link_text("Home")

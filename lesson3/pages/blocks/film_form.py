__author__ = 'user'

from lesson3.pages.page import Page
from selenium.webdriver.support.select import Select


class FilmForm(Page):

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
    def note_field(self):
        return self.driver.find_element_by_name("notes")

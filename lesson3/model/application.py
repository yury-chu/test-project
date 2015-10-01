# -*- coding: utf-8 -*-

import time
import random

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import *
from lesson3.pages.login_page import LoginPage
from lesson3.pages.internal_page import InternalPage
from lesson3.pages.film_management_page import FilmManagementPage


class Application(object):

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.login_page = LoginPage(driver)
        self.internal_page = InternalPage(driver)
        self.film_management_page = FilmManagementPage(driver)

    # ---------------Здесь вспомогательные методы для тестов----------------
    def give_find_field(self):
        """
        Возвращает очищенное поле поиска для работы с ним
        """
        driver = self.driver
        elem = driver.find_element_by_xpath("//div[@class='searchbox']/input")
        elem.send_keys(Keys.CONTROL, "a")
        time.sleep(1)
        elem.send_keys(Keys.BACK_SPACE)
        elem.clear()  # продублируем очистку поля на всякий случай
        return elem

    def login_in_system(self, user):
        """
        Вход в систему
        """
        driver = self.driver
        driver.get("http://localhost/test_app/public_html/php4dvd/")
        lp = self.login_page
        if self.is_not_logged_in():
            lp.username_field.send_keys(user.username)
            lp.password_field.send_keys(user.password)
            lp.submit_button.click()
        else:
            self.logout()
            lp.username_field.send_keys(user.username)
            lp.password_field.send_keys(user.password)
            lp.submit_button.click()

    def logout(self):
        """
        Выходит из системы
        """
        self.internal_page.logout_button.click()
        self.wait.until(alert_is_present()).accept()

    def fill_movie_form(self, param, btn=False, go_main=False):
        """
        Заливает поля добавления фильма, может нажимать кнопку и преходить на главную
        """
        fm = self.film_management_page

        fm.go_to_film_management.click()
        fm.name_field.clear()
        fm.name_field.send_keys(param.name)

        fm.year_field.clear()
        fm.year_field.send_keys(param.year)

        fm.frmt_field.clear()
        fm.frmt_field.send_keys(param.frmt)

        fm.note_feild.clear()
        fm.note_feild.send_keys(param.note)

        if btn:
            fm.button_save.click()

        if go_main:
            fm.link_to_main_page.click()

    def films_on_main_page(self):
        """
        Сколько записей фильмов на главной
        """
        driver = self.driver
        driver.find_element_by_link_text("Home").click()
        films = driver.find_elements_by_xpath("//div[@class='nocover']")
        return len(films)

    def give_this_film(self, film):
        """
        Переходит на принятый в параметре фильм
        """
        driver = self.driver
        driver.find_element_by_link_text("Home").click()
        driver.find_element_by_xpath("//div[@title=\"%s\"]" % film.name).click()
        # если есть, и можно кликнуть, то все хорошо

    def verify_no_movies(self):
        """
        Применяется, когда надо получить с главной страницы текст, то что ничего не найдено
        """
        driver = self.driver
        driver.find_element_by_link_text("Home").click()
        content = driver.find_element_by_class_name("content")
        return content.text

    def find_film(self, film):
        """
        Вводит в поле поиска преданный в параметре фильм и жмет enter
        """
        find_field = self.give_find_field()
        find_field.send_keys(film.name)
        find_field.send_keys(Keys.RETURN)
        time.sleep(3)

    def header_now_added_film(self):
        """
        Получает заголовок вновь созаднного фильма
        """
        driver = self.driver
        return driver.find_element_by_xpath("//div[@class='maininfo_full']/h2").text

    def film_exist_on_main_page(self, film):
        """
        Убеждается, что фильм есть на главной странице
        """
        driver = self.driver
        driver.find_element_by_link_text("Home").click()
        driver.find_element_by_xpath("//div[@title=\"%s\"]" % film.name).click()

    def clear_and_check_required_fields(self):
        """
        Чистит обязательные поля и проверяет, выдалось ли сообщение об обязательности их после клика
        """
        driver = self.driver
        req_fields = driver.find_elements_by_class_name("required")
        for elem in req_fields:
            elem.clear()  # зачистили все поля, обозначенные как уникальные

        driver.find_element_by_name("submit").click()

        # проверим, что выдались предупреждения об обязательных полях
        err_labels = driver.find_elements_by_xpath("//label[@class='error']")
        for elem in err_labels:
            assert (elem.text, "This field is required")

    def give_random_film(self):
        """
        Выбирает случайный фильм и кликает по нему
        """
        driver = self.driver
        driver.find_element_by_link_text("Home").click()
        boxes = driver.find_elements_by_xpath("//div[@class='nocover']")
        count = len(boxes)
        random_count = random.randint(0, count-1)
        box = boxes[random_count]
        box.click()

    def remove_film(self):
        """
        Удаляет фильм, соглашается с alert
        """
        driver = self.driver
        driver.find_element_by_xpath("//img[@title='Remove']").click()
        alert = driver.switch_to_alert()
        alert.accept()

    def is_logged_in(self):
        """
        Проверяет, залогинены лы мы в системе
        """
        driver = self.driver
        try:
            self.wait.until(presence_of_element_located((By.CSS_SELECTOR, "nav")))
            return True
        except WebDriverException:
            return False

    def is_not_logged_in(self):
        try:
            self.wait.until(presence_of_element_located((By.ID, "loginform")))
            return True
        except WebDriverException:
            return False


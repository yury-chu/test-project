# -*- coding: utf-8 -*-

import time
import random
from selenium.webdriver.common.keys import Keys

class Application(object):

    def __init__(self, driver):
        self.driver = driver

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
        driver.find_element_by_id("username").send_keys(user.username)
        driver.find_element_by_name("password").send_keys(user.password)
        driver.find_element_by_name("submit").click()

    def fill_movie_form(self, param, btn=False, go_main=False):
        """
        Заливает поля добавления фильма, может нажимать кнопку и преходить на главную
        """
        driver = self.driver
        driver.find_element_by_css_selector("img[alt=\"Add movie\"]").click()
        driver.find_element_by_name("name").clear()
        driver.find_element_by_name("name").send_keys(param.name)

        driver.find_element_by_name("year").clear()
        driver.find_element_by_name("year").send_keys(param.year)

        driver.find_element_by_name("format").clear()
        driver.find_element_by_name("format").send_keys(param.frmt)

        driver.find_element_by_name("notes").clear()
        driver.find_element_by_name("notes").send_keys(param.note)

        if btn:
            driver.find_element_by_name("submit").click()

        if go_main:
            driver.find_element_by_link_text("Home").click()

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

# -*- coding: utf-8 -*-
__author__ = 'user'

import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.expected_conditions import *


class AddRmFilmTest(unittest.TestCase):
    """
    Разработать тест для добавления и удаления описания фильма
    """
    def setUp(self):
        self.driver = webdriver.Firefox()

    def test_add_film_good_data(self):
        driver = self.driver
        film_name = u"Терминатор"
        film_year = "1984"

        self.login_in_system()

# на всякий случай создадим фильм
        self.add_film(film_name, film_year)
        # проверяем, что фильм добавился

        h2 = driver.find_element_by_xpath("//div[@id='movie']/div[2]/h2")
        title_name = u"Терминатор (1984)"
        self.assertEqual(title_name, h2.text)

        # выбираем фильм с главной страницы
        driver.find_element_by_link_text("Home").click()

        driver.find_element_by_xpath(
            "//div[@class='movie_box']/div[@class='movie_cover']/div[@alt='Терминатор']"
        ).click()
        # заходим на редактирование
        driver.find_element_by_css_selector("img[alt=\"Edit\"]").click()

        # добавляем personal notes
        personal_notes = u"Эффект дыма, поднимающегося от куртки Шварценеггера"
        driver.find_element_by_name("notes").clear()  # на всякий случай очистим поле
        driver.find_element_by_name("notes").send_keys(personal_notes)  # ввели описание
        driver.find_element_by_name("submit").click()
        # проверяем, что описание добавилось
        notes = driver.find_element_by_class_name("notes")
        self.assertEqual(notes.text, u"Personal notes\n" + personal_notes)

        # переходим на редактирование для удалением personal notes
        driver.find_element_by_css_selector("img[alt=\"Edit\"]").click()

        driver.find_element_by_name("notes").clear()  # удаляем описание
        driver.find_element_by_name("submit").click()


        finded = ""
        try:
            finded = driver.find_element_by_class_name("notes").text
        except:
            pass

        if finded == (u"Personal notes\n" + personal_notes):
            raise AssertionError

    def clear_and_check_required_feilds(self):
        """
        Чистит обязательные поля и проверяет, выдалось ли сообщение об обязательности их после клика
        """
        driver = self.driver
        req_fields = driver.find_elements_by_class_name("required")
        for elem in req_fields:
            elem.clear()
        driver.find_element_by_name("submit").click()
# проверим, что выдались предупреждения об обязательных полях
        err_labels = driver.find_elements_by_xpath("//label[@class='error']")
        for elem in err_labels:
            self.assertEqual(elem.text, "This field is required")

    def login_in_system(self):
        """
        Вход в систему
        """
        driver = self.driver
        # вход в систему
        driver.get("http://localhost/test_app/public_html/php4dvd/")
        driver.find_element_by_id("username").send_keys("admin")
        driver.find_element_by_name("password").send_keys("admin")
        driver.find_element_by_name("submit").click()

    def add_film(self, name, year, frmt="DVD"):
        """
        Добавляет фильм из главной страницы
        :param name: Название фильма
        :param year: год фильма
        :param frmt: формат фильма, есть значение по умолчанию.
        """
        driver = self.driver
        driver.implicitly_wait(3)

        driver.find_element_by_css_selector("img[alt=\"Add movie\"]").click()
        driver.find_element_by_name("name").clear()
        driver.find_element_by_name("name").send_keys(name)

        driver.find_element_by_name("year").clear()
        driver.find_element_by_name("year").send_keys(year)

        driver.find_element_by_name("format").clear()
        driver.find_element_by_name("format").send_keys(frmt)

        driver.find_element_by_name("submit").click()

    def tearDown(self):
        #self.driver.quit()
        pass

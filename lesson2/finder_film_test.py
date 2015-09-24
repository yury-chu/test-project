# -*- coding: utf-8 -*-
__author__ = 'user'

import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.expected_conditions import *


class FinderFilmTest(unittest.TestCase):
    """
    Разработать тест для добавления и удаления описания фильма
    """
    def setUp(self):
        self.driver = webdriver.Firefox()

    def test_film_finded(self):
        driver = self.driver

        # вход в систему
        driver.get("http://localhost/test_app/public_html/php4dvd/")
        driver.find_element_by_id("username").send_keys("admin")
        driver.find_element_by_name("password").send_keys("admin")
        driver.find_element_by_name("submit").click()

        # добавим фильм, который потом будем искать
        driver.find_element_by_css_selector("img[alt=\"Add movie\"]").click()
        # заносим минимальные данные
        film_name = u"Терминатор"
        film_year = u"1984"
        driver.find_element_by_name("name").send_keys(film_name)
        driver.find_element_by_name("year").send_keys(film_year)
        driver.find_element_by_name("submit").click()

        # переходим на главную
        driver.find_element_by_link_text("Home").click()
        elem = driver.find_element_by_xpath("//div[@class='searchbox']/input")
        elem.send_keys(film_name)
        elem.send_keys(Keys.RETURN)

        driver.implicitly_wait(3)
        finded = driver.find_elements_by_xpath("//div[@class='movie_cover']/div[@alt='" + film_name +"']")
        if len(finded) > 0:
            pass  # элементы нашлись
        else:
            raise AssertionError

        # теперь проверим, что не находится фильм, которого нету в каталоге
        # зачищаем поле поиска
        elem.send_keys(Keys.CONTROL, "a")
        time.sleep(1)
        elem.send_keys(Keys.BACK_SPACE)
        elem.send_keys(Keys.RETURN)

        driver.find_element_by_link_text("Home").click()
        driver.implicitly_wait(3)

        no_finded_film = u"Планета обезьян"
        finded_elems = []
        try:
            finded_elems = driver.find_elements_by_xpath("//div[@title='" + no_finded_film + "']")
        except:
            pass
        if len(finded_elems) > 0:
            raise AssertionError, "Такой фильм уже есть, тест будет не точным"

        # если дошли, то можно искать этот фильм с ожидаемым результатом, что ничего не найдено
        elem = driver.find_element_by_xpath("//div[@class='searchbox']/input")
        elem.send_keys(no_finded_film)
        elem.send_keys(Keys.RETURN)
        driver.implicitly_wait(3)
        bad_find_result = driver.find_element_by_class_name("content")
        if bad_find_result.text == "No movies where found.":
            pass #  действительно ничего не нашлось
        else:
            assert AssertionError, "Нашелся какой то фмльм, которого не должно быть"

    def tearDown(self):
        self.driver.quit()


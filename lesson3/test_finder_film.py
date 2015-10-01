# -*- coding: utf-8 -*-
__author__ = 'user'

import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.expected_conditions import *

from selenium import webdriver
from selenium_fixture import driver
from model.user import User
from model.film import Film


def test_find_good(driver):
    """
    Тест с ожидаемым пололжительным результатом, что фильм найдется
    """
    # вход в систему
    login_in_system(driver, User.Admin())

    # добавим два фильма для тестирования поиска
    fill_movie_form(driver, Film.goneWind(), True, True)  # первый
    fill_movie_form(driver, Film.weryDanger(), True, True)  # второй

    # смотрим и запоминаем сколько есть фильмов
    movie_boxes = driver.find_elements_by_xpath("//div[@class='nocover']")
    first_len_boxes = len(movie_boxes)

    # получим поле поиска
    find_field = give_find_field(driver)

    # поищем первый фильм по поиску
    find_field.send_keys(Film.goneWind().name)
    find_field.send_keys(Keys.RETURN)
    time.sleep(3)

    # смотрим и запоминаем сколько стало фильмов
    movie_boxes = driver.find_elements_by_xpath("//div[@class='nocover']")
    last_len_boxes = len(movie_boxes)

    # сравниваем до и после, если изменилось, поиск работает, но необходимо убедиться, что нашлось, то что нужно
    if first_len_boxes == last_len_boxes:
        raise AssertionError, u"Количество фильмов не изменилось, возможно поиск не работает"
    else:
        # проверим, если тут искомый фильм
        driver.find_element_by_xpath("//div[@title=\"%s\"]" % Film.goneWind().name).click()
        # если есть, и можно кликнуть, то все хорошо


def test_find_bad(driver):
    """
    Тест с ожидаемым отрицательным результатом, что фильм не найдется
    """
    # вход в систему
    login_in_system(driver, User.Admin())

    # добавим два фильма для тестирования поиска
    fill_movie_form(driver, Film.goodFilm(), True, True)
    fill_movie_form(driver, Film.veryGoodFilm(), True, True)

    # попробуем поискать несуществующий фильм, но сначала убедимся, что его нету в каталоге
    try:
        driver.find_element_by_xpath("//div[@title=\"%s\"]" % Film.randomFilm().name).click()
        so_bad = 1
    except NoSuchElementException:
        # если не получилось найти, то можно проверять поиск по нему
        so_bad = 0

    if so_bad == 0:
        # получим поле поиска
        find_field = give_find_field(driver)
        # поищем рандомный фильм по поиску
        find_field.send_keys(Film.randomFilm().name)
        find_field.send_keys(Keys.RETURN)
        time.sleep(3)

        # Убедимся, что не отображается никаких найденных фильмов на странице
        no_movies = driver.find_element_by_class_name("content").text
        assert (no_movies, "No movies where found.")

    if so_bad == 1:
        raise AssertionError, u"Нашелся какой то фильм, нужно взять на тестирование несуществующий"


# ---------------Здесь вспомогательные методы для тестов----------------

def give_find_field(driver):
    """
    Возвращает очищенное поле поиска для работы с ним
    """
    elem = driver.find_element_by_xpath("//div[@class='searchbox']/input")
    elem.send_keys(Keys.CONTROL, "a")
    time.sleep(1)
    elem.send_keys(Keys.BACK_SPACE)
    elem.clear()  # продублируем очистку поля на всякий случай
    return elem


def login_in_system(driver, user):
    """
    Вход в систему
    """
    # вход в систему
    driver.get("http://localhost/test_app/public_html/php4dvd/")
    driver.find_element_by_id("username").send_keys(user.username)
    driver.find_element_by_name("password").send_keys(user.password)
    driver.find_element_by_name("submit").click()


def fill_movie_form(driver, param, btn=False, go_main=False):
    """
    Заливает поля добавления фильма, может нажимать кнопку и преходить на главную
    """
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

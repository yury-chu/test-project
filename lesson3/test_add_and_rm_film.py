# -*- coding: utf-8 -*-
__author__ = 'user'

import unittest
import random
from selenium import webdriver
from selenium.webdriver.support.expected_conditions import *

from selenium_fixture import driver
from model.user import User


def test_create_film_good(driver):
    """
    Создает фильм
    """
    # инициализируем данные для фильма
    film_param = {
        'name': u"Мадагаскар",
        'year': u"2000",
        'format': u"DVD",
        'note': u"Описание фильма, необязательное поле Personal notes"
    }
    login_in_system(driver, User.Admin())
    fill_movie_form(driver, film_param, True)
    #  проверим, что правильно занеслись данные
    title_elem = driver.find_element_by_xpath("//div[@class='maininfo_full']/h2").text
    valid_title_elem = film_param['name'] + " (" + film_param['year'] + ")"  # формируем проверочную строку
    assert (title_elem, valid_title_elem)

    #  проверим, что он отображается на главной странице
    driver.find_element_by_link_text("Home").click()
    driver.find_element_by_xpath("//div[@title=\"%s\"]" % film_param['name']).click()


def test_create_film_bad(driver):
    """
    Пробует создать фильм с незаполненными обязательными полями
    """
    # инициализируем данные для фильма
    film_param = {
        'name': u"Пираты карибского моря",
        'year': u"2001",
        'format': u"DVD",
        'note': u"Описание фильма, необязательное поле Personal notes"
    }
    login_in_system(driver, User.Admin())
    fill_movie_form(driver, film_param)
    clear_and_check_required_feilds(driver)


def test_delete_film(driver):
    """
    Удаляет фильм из каталога
    """
    login_in_system(driver, User.Admin())
    movie_boxes = driver.find_elements_by_xpath("//div[@class='nocover']")
    first_len = len(movie_boxes)
    if first_len != 0:
        removing_film = give_random_film(driver, movie_boxes)
        removing_film.click()
        driver.find_element_by_xpath("//img[@title='Remove']").click()
        alert = driver.switch_to_alert()
        alert.accept()

        # проверяем, сколько теперь нашлось фильмов
        if first_len == 1:  # если был один фильм, то на главной теперь пусто, ищем это утверждение
            no_movies = driver.find_element_by_class_name("content").text
            assert (no_movies, "No movies where found.")
            last_len = 0  # длину найденных элементов делаем 0
        else:
            movie_boxes = driver.find_elements_by_xpath("//div[@class='movie_box']")
            last_len = len(movie_boxes)

        if first_len == last_len:
            raise AssertionError, u"Фильм не удалился"
    else:
        raise NoSuchElementException, u"Нечего удалять"


# ----------------- вспомогательные методы ---------------------

def login_in_system(driver, user):
    """
    Вход в систему
    """
    driver.get("http://localhost/test_app/public_html/php4dvd/")
    driver.find_element_by_id("username").send_keys(user.username)
    driver.find_element_by_name("password").send_keys(user.password)
    driver.find_element_by_name("submit").click()


def fill_movie_form(driver, param, btn=False):
    """
    Добавляет фильм
    """
    driver.find_element_by_css_selector("img[alt=\"Add movie\"]").click()
    driver.find_element_by_name("name").clear()
    driver.find_element_by_name("name").send_keys(param["name"])

    driver.find_element_by_name("year").clear()
    driver.find_element_by_name("year").send_keys(param["year"])

    driver.find_element_by_name("format").clear()
    driver.find_element_by_name("format").send_keys(param["format"])

    driver.find_element_by_name("notes").clear()
    driver.find_element_by_name("notes").send_keys(param["note"])

    if btn == True:
        driver.find_element_by_name("submit").click()


def clear_and_check_required_feilds(driver):
    """
    Чистит обязательные поля и проверяет, выдалось ли сообщение об обязательности их после клика
    """
    req_fields = driver.find_elements_by_class_name("required")
    for elem in req_fields:
        elem.clear()  # зачистим все поля, обозначенные как уникальные

    driver.find_element_by_name("submit").click()
    # проверим, что выдались предупреждения об обязательных полях
    err_labels = driver.find_elements_by_xpath("//label[@class='error']")
    for elem in err_labels:
        assert (elem.text, "This field is required")


def give_random_film(driver, boxes):
    count = len(boxes)
    random_count = random.randint(0, count-1)
    box = boxes[random_count]
    return box

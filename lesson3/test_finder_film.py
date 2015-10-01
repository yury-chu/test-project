# -*- coding: utf-8 -*-
__author__ = 'user'

from selenium.webdriver.support.expected_conditions import *

from selenium import webdriver
from selenium_fixture import app
from model.user import User
from model.film import Film


def test_find_good(app):
    """
    Тест с ожидаемым пололжительным результатом, что фильм найдется
    """
    # вход в систему
    app.login_in_system(User.Admin())

    # добавим два фильма для тестирования поиска
    app.fill_movie_form(Film.goneWind(), True, True)  # первый
    app.fill_movie_form(Film.weryDanger(), True, True)  # второй

    # смотрим и запоминаем сколько есть фильмов
    first_len_boxes = app.films_on_main_page()

    # поищем первый фильм по поиску
    app.find_film(Film.goneWind())

    # смотрим и запоминаем сколько стало фильмов
    last_len_boxes = app.films_on_main_page()

    # сравниваем до и после, если изменилось, поиск работает, но необходимо убедиться, что нашлось, то что нужно
    if first_len_boxes == last_len_boxes:
        raise AssertionError, u"Количество фильмов не изменилось, возможно поиск не работает"
    else:
        # проверим, если тут искомый фильм
        app.give_this_film(Film.goneWind())
        # если есть, и можно кликнуть, то все хорошо


def test_find_bad(app):
    """
    Тест с ожидаемым отрицательным результатом, что фильм не найдется
    """
    # вход в систему
    app.login_in_system(User.Admin())

    # добавим два фильма для тестирования поиска
    app.fill_movie_form(Film.goodFilm(), True, True)
    app.fill_movie_form(Film.veryGoodFilm(), True, True)

    # попробуем поискать несуществующий фильм, но сначала убедимся, что его нету в каталоге
    try:
        app.give_this_film(Film.randomFilm())
        so_bad = 1
    except NoSuchElementException:
        # если не получилось найти, то можно проверять поиск по нему
        so_bad = 0

    if so_bad == 0:
        # поищем рандомный фильм по поиску
        app.find_film(Film.randomFilm())

        # Убедимся, что не отображается никаких найденных фильмов на странице
        no_movies = app.verify_no_movies()
        assert (no_movies, "No movies where found.")

    if so_bad == 1:
        raise AssertionError, u"Нашелся какой то фильм, нужно взять на тестирование несуществующий"

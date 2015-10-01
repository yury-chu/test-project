# -*- coding: utf-8 -*-
__author__ = 'user'


from selenium.webdriver.support.expected_conditions import *

from selenium_fixture import app
from model.user import User
from model.film import Film


def test_create_film_good(app):
    """
    Проверяет создание фильма
    """
    app.login_in_system(User.Admin())
    app.fill_movie_form(Film.madagaskar(), True)

    #  проверим, что правильно занеслись данные
    title_elem = app.header_now_added_film()
    valid_title_elem = Film.madagaskar().name + " (" + Film.madagaskar().year + ")"  # формируем проверочную строку
    assert (title_elem, valid_title_elem)

    #  проверим, что он отображается на главной странице и на него можно перейти
    app.film_exist_on_main_page(Film.madagaskar())
    app.logout()


def test_create_film_bad(app):
    """
    Пробует создать фильм с незаполненными обязательными полями
    """
    app.login_in_system(User.Admin())
    app.fill_movie_form(Film.pirates())
    app.clear_and_check_required_fields()
    app.logout()


def test_delete_film(app):
    """
    Проверяет удаление фильма из каталога
    """
    app.login_in_system(User.Admin())
    first_len = app.films_on_main_page()  # узнаем сколько фильмо есть в системе
    if first_len != 0:
        app.give_random_film()  # если что то есть, выберем случайный, (кликнет по нему)
        app.remove_film()  # удалим фильм

        # проверяем, сколько теперь нашлось фильмов
        if first_len == 1:  # если был один фильм, то на главной теперь пусто, ищем это утверждение
            no_movies = app.verify_no_movies()
            assert (no_movies, "No movies where found.")
            last_len = 0  # длину найденных элементов делаем 0
        else:
            last_len = app.films_on_main_page()

        if first_len == last_len:
            raise AssertionError, u"Фильм не удалился"
    else:
        raise NoSuchElementException, u"Нечего удалять"
    app.logout()

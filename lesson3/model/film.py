# -*- coding: utf-8 -*-
__author__ = 'user'


class Film(object):
    """
    Содержит используемые в тестах фильмы
    """

    def __init__(self, name="", year="", frmt="", note=""):
        self.name = name
        self.year = year
        self.frmt = frmt
        self.note = note

    @classmethod
    def madagaskar(cls):
        return cls(name=u"Мадагаскар",
                   year=u"2000",
                   frmt=u"DVD",
                   note=u"Описание фильма, необязательное поле Personal notes",
                   )

    @classmethod
    def pirates(cls):
        return cls(name=u"Пираты карибского моря",
                   year=u"2001",
                   frmt=u"DVD",
                   note=u"Описание фильма, необязательное поле Personal notes",
                   )

    @classmethod
    def goneWind(cls):
        return cls(name=u"Унесенные ветром",
                   year=u"1990",
                   frmt=u"DVD",
                   note=u"Описание фильма, необязательное поле Personal notes",
                   )

    @classmethod
    def weryDanger(cls):
        return cls(name=u"Особо опасен",
                   year=u"2010",
                   frmt=u"DVD",
                   note=u"Описание фильма, необязательное поле Personal notes",
                   )

    @classmethod
    def goodFilm(cls):
        return cls(name=u"Хороший фильм",
                   year=u"1991",
                   frmt=u"DVD",
                   note=u"Описание фильма, необязательное поле Personal notes",
                   )

    @classmethod
    def veryGoodFilm(cls):
        return cls(name=u"Самый лучший фильм",
                   year=u"2010",
                   frmt=u"DVD",
                   note=u"Описание фильма, необязательное поле Personal notes",
                   )

    @classmethod
    def randomFilm(cls):
        return cls(name=u"Абракадабра100500",
                   year=u"0001",
                   frmt=u"dont know",
                   note=u"Описание фильма, необязательное поле Personal notes",
                   )

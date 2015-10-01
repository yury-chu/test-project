# -*- coding: utf-8 -*-
__author__ = 'user'

from selenium import webdriver
import pytest
from model.application import Application


@pytest.fixture
def app(request):
    driver = webdriver.Firefox()
    driver.implicitly_wait(10)
    request.addfinalizer(driver.quit)
    return Application(driver)

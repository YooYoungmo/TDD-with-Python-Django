# -*- coding: utf-8 -*-
from selenium import webdriver

__author__ = 'yooyoung-mo'

browser = webdriver.Firefox()
browser.get('http://localhost:8000')

assert 'Django' in browser.title
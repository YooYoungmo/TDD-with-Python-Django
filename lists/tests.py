# -*- coding: utf-8 -*-

from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase

from lists.views import home_page


class HomePageTest(TestCase):
    def test_root_url_resovles_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)

        expected_html = render_to_string('home.html')

        self.assertEqual(response.content.decode('utf-8'), expected_html)

    def test_home_page_can_save_a_POST_request(self):
        # given
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = u'신규 작업 아이템'

        # when
        response = home_page(request)

        # then
        self.assertIn(u'신규 작업 아이템', response.content.decode('utf-8'))

        expected_html = render_to_string('home.html', {'new_item_text': u'신규 작업 아이템'})
        self.assertEqual(response.content.decode('utf-8'), expected_html)
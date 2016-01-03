# -*- coding: utf-8 -*-

from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase

from lists.models import Item
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


class ItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.text = u'첫 번째 아이템'
        first_item.save()

        second_item = Item()
        second_item.text = u'두 번째 아이템'
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, u'첫 번째 아이템')
        self.assertEqual(second_saved_item.text, u'두 번째 아이템')


class ListViewTest(TestCase):
    def test_uses_list_template(self):
        response = self.client.get('/lists/the-only-list-in-the-world/')
        self.assertTemplateUsed(response, 'list.html')

    def test_home_page_displays_all_list_items(self):
        # given
        Item.objects.create(text='itemey 1')
        Item.objects.create(text='itemey 2')

        # when
        response = self.client.get('/lists/the-only-list-in-the-world/')

        # then
        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')

    def test_home_page_can_save_a_POST_request(self):
        # given, when
        self.client.post('/lists/new', data={'item_text': u'신규 작업 아이템'})

        # then
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, u'신규 작업 아이템')

    def test_home_page_redirects_after_POST(self):
        # given, when
        response = self.client.post('/lists/new', data={'item_text': u'신규 작업 아이템'})

        # then
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/lists/the-only-list-in-the-world/')
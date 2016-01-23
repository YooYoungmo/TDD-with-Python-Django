# -*- coding: utf-8 -*-
from django.test import TestCase

from lists.forms import ItemForm, EMPTY_LIST_ERROR

__author__ = 'yooyoung-mo'


class ItemFormTest(TestCase):
    def test_form_renders_item_text_input(self):
        form = ItemForm()
        self.assertIn(u'placeholder="작업 아이템 입력"', form.as_p())
        self.assertIn('class="form-control input-lg"', form.as_p())
        self.assertIn('id="id_new_item"', form.as_p())

    def test_form_validation_for_blank_items(self):
        form = ItemForm(data={'text': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'],
                         [EMPTY_LIST_ERROR])
# -*- coding: utf-8 -*-
from django.test import TestCase

from lists.forms import ItemForm, EMPTY_LIST_ERROR, DUPLICATE_ITEM_ERROR, ExistingListItemForm
from lists.models import List, Item

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

    def test_form_save_handles_saving_to_a_list(self):
        list_ = List.objects.create()
        form = ItemForm(data={'text': 'do me'})
        new_item = form.save(for_list=list_)
        self.assertEqual(new_item, Item.objects.first())
        self.assertEqual(new_item.text, 'do me')
        self.assertEqual(new_item.list, list_)


class ExistingListItemFormTest(TestCase):
    def test_form_renders_item_text_input(self):
        list_ = List.objects.create()
        form = ExistingListItemForm(for_list=list_)
        self.assertIn(u'placeholder="작업 아이템 입력"', form.as_p())

    def test_form_validation_for_blank_items(self):
        list_ = List.objects.create()
        form = ExistingListItemForm(for_list=list_, data={'text': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [EMPTY_LIST_ERROR])

    def test_form_validation_for_duplicate_items(self):
        list_ = List.objects.create()
        Item.objects.create(list=list_, text=u'중복 금지!')
        form = ExistingListItemForm(for_list=list_, data={'text': u'중복 금지!'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [DUPLICATE_ITEM_ERROR])

    def test_form_save(self):
        list_ = List.objects.create()
        form = ExistingListItemForm(for_list=list_, data={'text': 'hi'})
        new_item = form.save()
        self.assertEqual(new_item, Item.objects.all().first())


class ItemFormAndExistingListItemForm(TestCase):
    def test_from_items_order(self):
        list_ = List.objects.create()
        ItemForm(data={'text': u'우유 사기'}).save(for_list=list_)
        ExistingListItemForm(for_list=list_, data={'text': u'tea 만들기'}).save()

        actual = List.objects.get(id=list_.id)

        self.assertEqual(actual.item_set.all()[0].text, u'우유 사기')
        self.assertEqual(actual.item_set.all()[1].text, u'tea 만들기')

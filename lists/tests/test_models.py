# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from lists.models import Item, List

User = get_user_model()


class ItemModelTest(TestCase):
    def test_string_representation(self):
        item = Item(text=u'어떤 테스트')
        self.assertEqual(str(item), '어떤 테스트')

    def test_default_text(self):
        item = Item()
        self.assertEqual(item.text, '')


class ListModelTest(TestCase):
    def test_get_absolute_url(self):
        list_ = List.objects.create()
        self.assertEqual(list_.get_absolute_url(), '/lists/%d/' % (list_.id,))

    def test_create_new_creates_list_and_first_item(self):
        List.create_new(first_item_text=u'신규 아이템 텍스트')
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, u'신규 아이템 텍스트')
        new_list = List.objects.first()
        self.assertEqual(new_item.list, new_list)

    def test_create_new_optionally_saves_owner(self):
        user = User.objects.create()
        List.create_new(first_item_text=u'신규 아이템 텍스트', owner=user)
        new_list = List.objects.first()
        self.assertEqual(new_list.owner, user)

    def test_list_can_have_owners(self):
        List(owner=User())

    def test_list_owner_is_optional(self):
        List().full_clean()

    def test_create_returns_new_list_object(self):
        returned = List.create_new(first_item_text=u'신규 아이템 텍스트')
        new_list = List.objects.first()
        self.assertEqual(returned, new_list)

    def test_list_name_is_first_item_text(self):
        list_ = List.objects.create()
        Item.objects.create(list=list_, text=u'첫 번쩨 아이템')
        Item.objects.create(list=list_, text=u'두 번쩨 아이템')
        self.assertEqual(list_.name, u'첫 번쩨 아이템')


class ListAndItemModelsTest(TestCase):
    def test_item_is_related_to_list(self):
        list_ = List.objects.create()
        item = Item()
        item.list = list_
        item.save()
        self.assertIn(item, list_.item_set.all())

    def test_cannot_save_empty_list_items(self):
        list_ = List.objects.create()
        item = Item(list=list_, text='')
        with self.assertRaises(ValidationError):
            item.full_clean()
            item.save()

    def test_duplicate_items_are_invalid(self):
        list_ = List.objects.create()
        Item.objects.create(list=list_, text='bla')
        with self.assertRaises(ValidationError):
            item = Item(list=list_, text='bla')
            item.full_clean()

    def test_CAN_save_same_item_to_different_lists(self):
        list1 = List.objects.create()
        list2 = List.objects.create()
        Item.objects.create(list=list1, text='bla')
        item = Item(list=list2, text='bla')
        item.full_clean()

    def test_list_ordering(self):
        list1 = List.objects.create()
        item1 = Item.objects.create(list=list1, text='i1')
        item2 = Item.objects.create(list=list1, text='item 2')
        item3 = Item.objects.create(list=list1, text='3')

        actual = List.objects.get(id=list1.id)
        self.assertEqual(list(actual.item_set.all()), [item1, item2, item3])



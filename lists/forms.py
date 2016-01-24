# -*- coding: utf-8 -*-
from django import forms
from django.core.exceptions import ValidationError
from django.forms.utils import ErrorList

from lists.models import Item

__author__ = 'yooyoung-mo'

EMPTY_LIST_ERROR = "You can't have an empty list item"
DUPLICATE_ITEM_ERROR = u'이미 리스트에 해당 아이템이 있습니다'


class ItemForm(forms.models.ModelForm):
    def save(self, for_list, commit=True):
        self.instance.list = for_list
        return super(ItemForm, self).save(commit)

    class Meta:
        model = Item
        fields = ('text',)
        widgets = {
            'text': forms.fields.TextInput(attrs={
                'placeholder': u'작업 아이템 입력',
                'class': 'form-control input-lg',
                'id': 'id_new_item'
            })
        }
        error_messages = {
            'text': {'required': EMPTY_LIST_ERROR}
        }


class ExistingListItemForm(ItemForm):
    def __init__(self, for_list, data=None, files=None, auto_id='id_%s', prefix=None, initial=None, error_class=ErrorList,
                 label_suffix=None, empty_permitted=False, instance=None):
        super(ExistingListItemForm, self).__init__(data, files, auto_id, prefix, initial, error_class, label_suffix,
                                                   empty_permitted, instance)
        self.instance.list = for_list

    def validate_unique(self):
        try:
            self.instance.validate_unique()
        except ValidationError as e:
            e.error_dict = {'text': [DUPLICATE_ITEM_ERROR]}
            self._update_errors(e)
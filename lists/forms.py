# -*- coding: utf-8 -*-
from django import forms

from lists.models import Item

__author__ = 'yooyoung-mo'

EMPTY_LIST_ERROR = "You can't have an empty list item"


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
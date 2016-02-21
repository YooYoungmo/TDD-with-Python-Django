# -*- coding: utf-8 -*-
from django.test import TestCase
from mock import patch
__author__ = 'yooyoung-mo'


class LoginViewTest(TestCase):

    @patch('accounts.views.authenticate')
    def test_called_authenticate_with_assertion_from_post(self, mock_authenticate):
        mock_authenticate.return_value = None
        self.client.post('/accounts/login', {'assertion': 'assert this'})
        mock_authenticate.assert_called_with(assertion='assert this')
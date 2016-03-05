# -*- coding: utf-8 -*-
import logging

from django.contrib.auth import get_user_model

__author__ = 'yooyoung-mo'
import requests

PERSONA_VERIFY_URL = 'https://verifier.login.persona.org/verify'
DOMAIN = 'localhost'

User = get_user_model()


class PersonaAuthenticationBackend:
    def __init__(self):
        pass

    def authenticate(self, assertion):
        logging.warn('authenticate 함수 진입')
        response = requests.post(
                PERSONA_VERIFY_URL,
                data={'assertion': assertion, 'audience': DOMAIN})
        logging.warn('퍼소나에서 응답 받음')
        logging.warn(response.content.decode())
        if response.ok and response.json()['status'] == 'okay':
            email = response.json()['email']
            try:
                return User.objects.get(email=email)
            except User.DoesNotExist:
                return User.objects.create(email=email)

    def get_user(self, email):
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None


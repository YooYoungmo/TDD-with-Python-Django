# -*- coding: utf-8 -*-
import logging

from django.conf import settings
from django.contrib.auth import get_user_model
import requests
__author__ = 'yooyoung-mo'

PERSONA_VERIFY_URL = 'https://verifier.login.persona.org/verify'
User = get_user_model()


class PersonaAuthenticationBackend:
    def __init__(self):
        pass

    def authenticate(self, assertion):
        logging.warn('authenticate 함수 진입')
        response = requests.post(
                PERSONA_VERIFY_URL,
                data={'assertion': assertion, 'audience': settings.DOMAIN})
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


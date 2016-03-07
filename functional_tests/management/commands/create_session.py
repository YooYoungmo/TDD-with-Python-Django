# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.auth import get_user_model, SESSION_KEY, BACKEND_SESSION_KEY
from django.contrib.sessions.backends.db import SessionStore
from django.core.management import BaseCommand

User = get_user_model()

__author__ = 'yooyoung-mo'


class Command(BaseCommand):
    def handle(self, email,  *args, **options):
        session_key = create_pre_authenticated_session(email)
        self.stdout.write(session_key)


def create_pre_authenticated_session(email):
    user = User.objects.create(email=email)
    session = SessionStore()
    session[SESSION_KEY] = user.pk
    session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
    session.save()
    return session.session_key
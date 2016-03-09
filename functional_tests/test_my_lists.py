# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.auth import get_user_model

from deploy_tools.server_tools import create_session_on_server
from functional_tests.base import FunctionalTest
from functional_tests.management.commands.create_session import create_pre_authenticated_session

__author__ = 'yooyoung-mo'

User = get_user_model()


class MyListsTest(FunctionalTest):

    def create_pre_authenticated_session(self, email):
        if self.against_staging:
            session_key = create_session_on_server(self.server_host, email)
        else:
            session_key = create_pre_authenticated_session(email)

        # # 쿠키를 설정하기 위해 도메인 접속이 필요하다
        # # 404 페이지가 뜬다
        self.browser.get(self.server_url + '/404_no_such_url/')
        self.browser.add_cookie(
            dict(
                name=settings.SESSION_COOKIE_NAME,
                value=session_key,
                path='/',
            )
        )

    def test_logged_in_users_lists_are_saved_as_my_lists(self):
        email = 'edith@example.com'
        self.browser.get(self.server_url)
        self.wait_to_be_logged_out(email)

        # 에디스가 사용자로 로그인 한다
        self.create_pre_authenticated_session(email)

        self.browser.get(self.server_url)
        self.wait_to_be_logged_in(email)
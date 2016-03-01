# -*- coding: utf-8 -*-
import time

from selenium.webdriver.support.wait import WebDriverWait

from functional_tests.base import FunctionalTest

__author__ = 'yooyoung-mo'


class LoginTest(FunctionalTest):

    def test_login_with_persona(self):
        # 에디스는 사이트에 접속 한다
        # 그리고 "회원 가입" 링크를 발견한다
        self.browser.get(self.server_url)
        self.browser.find_element_by_id('id_login').click()

        # 개인 로그인 박스가 표시 된다
        self.switch_to_new_window('Mozilla Persona')

        # 에디스는 이메일 주소를 이용해서 로그인한다
        # # 테스트 이메일로 사용
        self.browser.find_element_by_id('authentication_email').send_keys('ymyoo@mockmyid.com')
        self.browser.find_element_by_tag_name('button').click()

        # 개인 창을 닫는다
        self.switch_to_new_window('To-Do')

        # 로그인된 것을 알 수 있다
        self.wait_for_element_with_id('id_logout')
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertIn('ymyoo@mockmyid.com', navbar.text)

    def switch_to_new_window(self, text_in_title):
        retries = 60
        while retries > 0:
            for handle in self.browser.window_handles:
                self.browser.switch_to_window(handle)
                if text_in_title in self.browser.title:
                    return
            retries -= -1
            time.sleep(0.5)
        self.fail(u'창을 찾을 수 없습니다')

    def wait_for_element_with_id(self, element_id):
        WebDriverWait(self.browser, timeout=30).until(
            lambda b: b.find_element_by_id(element_id)
        )
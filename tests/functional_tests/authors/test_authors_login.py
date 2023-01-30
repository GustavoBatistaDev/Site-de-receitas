from time import sleep

import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .base import AuthorsBaseTest


@pytest.mark.functional_tests
class AuthorsLogintest(AuthorsBaseTest):
    def test_user_valid_data_can_login_successfully(self):
        string_password = '82077877Ab'
        user = User.objects.create_user(
            username='Gustav', password=string_password
        )
        self.browser.get(self.live_server_url + reverse('authors:login_view'))   
        sleep(2)
        form = self.browser.find_element(By.CLASS_NAME, 'main-form')

        username_field = self.browser.find_element(By.NAME, 'username')
        password_field = self.browser.find_element(By.NAME, 'password')
        username_field.send_keys(user.username)
        password_field.send_keys(string_password)
        sleep(2)

        password_field.send_keys(Keys.ENTER)

        self.assertIn(
            f'Your are logged in with {user.username}.',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )

    def test_login_create_raises_404_if_not_POST_method(self):
        self.browser.get(self.live_server_url+ reverse('authors:login_create')) # noqa
        body = self.browser.find_element(By.TAG_NAME, 'body')

        self.assertIn('Not Found', body.text)

    def test_if_message_invalid_username_or_password_appears(self):

        # fazendo a requisição para a pagina de login
        self.browser.get(self.live_server_url+ reverse('authors:login_view')) # noqa

        # selecionando input username
        username_field = self.browser.find_element(By.NAME, 'username')
        #  selecionando input password
        password_field = self.browser.find_element(By.NAME, 'password')

        #  digitando dados inválidos
        username_field.send_keys('    ')
        password_field.send_keys('    ')
        button = self.browser.find_element(By.ID, 'button-login')
        button.click()
        sleep(3)

        body = self.browser.find_element(By.TAG_NAME, 'body')

        self.assertIn('Invalid username or password.', body.text)

    def test_if_message_invalid_credentials_appears(self):

        # fazendo a requisição para a pagina de login
        self.browser.get(self.live_server_url+ reverse('authors:login_view')) # noqa

        # selecionando input username
        username_field = self.browser.find_element(By.NAME, 'username')
        #  selecionando input password
        password_field = self.browser.find_element(By.NAME, 'password')

        # digitando dados inválidos
        username_field.send_keys('teste1234')
        password_field.send_keys('teste1234Ab')
        button = self.browser.find_element(By.ID, 'button-login')
        button.click()
        sleep(3)

        body = self.browser.find_element(By.TAG_NAME, 'body')

        self.assertIn('invalid credentials.', body.text)


    # implementar teste do decorator
    #def test_no_login_required(self):

    #    self.client.login
    #    self.browser.get(self.live_server_url+ reverse('authors:login_view')) # noqa
    
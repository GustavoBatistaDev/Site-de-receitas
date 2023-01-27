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

        
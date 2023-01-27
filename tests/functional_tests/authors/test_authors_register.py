from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .base import AuthorsBaseTest


class AuthorsRegisterTest(AuthorsBaseTest):
    def execute_tests_by_name(self, field):
        return self.browser.find_element(
            By.NAME, field
        )

    def my_send_keys(self, campo, value):
        return campo.send_keys(
                value
            )

    def get_div_father_form(self):
        form = self.browser.find_element(By.XPATH, '/html/body/div/main/div[3]')  # noqa
        return form

    def test_the_error_if_invalid_forms(self):
        self.browser.get(self.live_server_url + '/authors/register/')
        username_input = self.execute_tests_by_name('username') 
        self.my_send_keys(username_input, '    ')
        sleep(1)

        first_name_input = self.execute_tests_by_name('first_name') 
        self.my_send_keys(first_name_input, ' ')
        sleep(1)

        last_name_input = self.execute_tests_by_name('last_name')
        self.my_send_keys(last_name_input, ' ')
        sleep(1)

        email_input = self.execute_tests_by_name('email') 
        self.my_send_keys(email_input, 'a.a@d.c')
        sleep(1)

        password = self.execute_tests_by_name('password') 
        self.my_send_keys(password, ' ')
        sleep(1)

        password2 = self.execute_tests_by_name('password2') 
        self.my_send_keys(password2, ' ')
        sleep(1)

        password2.send_keys(Keys.ENTER)

        sleep(2)

        form = self.get_div_father_form()
        self.assertIn('O campo First Name é obrigatório.', form.text) # noqa
        self.assertIn('O campo Last Name é obrigatório.', form.text) # noqa
        self.assertIn('Informe um endereço de email válido.', form.text) # noqa
       # self.assertIn('Password must be 8 characters long, including uppercase and lowercase letters.Password and password2 do not match', form.text) # noqa
        self.assertIn('Check the two password fields, please.', form.text) # noqa
        self.assertIn('O campo Username é obrigatório.', form.text) # noqa

    def test_user_register_if_data_to_correct(self):
        self.browser.get(self.live_server_url + '/authors/register/')
        username_input = self.execute_tests_by_name('username') 
        self.my_send_keys(username_input, 'Gustavo123')
        sleep(1)

        first_name_input = self.execute_tests_by_name('first_name') 
        self.my_send_keys(first_name_input, 'Gustavo')
        sleep(1)

        last_name_input = self.execute_tests_by_name('last_name')
        self.my_send_keys(last_name_input, 'Batista')
        sleep(1)

        email_input = self.execute_tests_by_name('email') 
        self.my_send_keys(email_input, 'gustavpip@gmail.com')
        sleep(1)

        password = self.execute_tests_by_name('password') 
        self.my_send_keys(password, '82077877Ab')
        sleep(1)

        password2 = self.execute_tests_by_name('password2') 
        self.my_send_keys(password2, '82077877Ab')
        sleep(1)

        password2.send_keys(Keys.ENTER)

        sleep(2)

        form = self.browser.find_element(By.XPATH, '/html/body/div/main')
        self.assertIn('Your user is created, please log in.', form.text)  # noqa
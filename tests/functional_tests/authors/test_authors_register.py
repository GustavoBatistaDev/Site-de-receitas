from .base import AuthorsBaseTest
from time import sleep


class AuthorsRegisterTest(AuthorsBaseTest):
    def test_yhe_test(self):
        self.browser.get(self.live_server_url + '/authors/register/')
        sleep(3)
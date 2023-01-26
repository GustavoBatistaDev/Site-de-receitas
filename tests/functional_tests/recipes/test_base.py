from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from utils.brownser import make_chrome_browser
import time
from recipes.tests.test_base_ import RecipeMixin


class RecipeBaseFunctionalTest(StaticLiveServerTestCase, RecipeMixin):
    def setUp(self) -> None:
        self.browser = make_chrome_browser()
        
        return super().setUp()

    def tearDown(self) -> None:
        self.browser.quit()
        return super().tearDown()

    def sleep(self, seconds=2):
        time.sleep(seconds)

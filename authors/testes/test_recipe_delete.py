from recipes.tests.test_base_ import RecipeMixin
from django.test import TestCase
from django.contrib.auth.models import User


class TestRecipeDelete(TestCase, RecipeMixin):
    def setUp(self) -> None:
        self.make_recipe()
        return super().setUp()

    def test_if_request_method_get_return_404(self):
        response = self.client.get('/dashboard/1/delete/')  # noqa
        self.assertEqual(response.status_code, 404)



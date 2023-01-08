from django.urls import reverse, resolve
from recipes import views
from .test_base_ import TestBase


class RecipeViewCategory(TestBase):

    # tests category
    def test_recipe_view_category_function_is_correct(self):

        view = resolve(reverse(
            'recipes:category', kwargs={'id': 1})
            )
        self.assertIs(view.func, views.category)

    def test_view_category_200_ok_if_category(self):

        self.make_recipe()
        response = self.client.get(
            reverse('recipes:category', kwargs={'id': 1})
            )
        self.assertEqual(response.status_code, 200)

    def test_view_category_loads_template_correct(self):
        
        self.make_recipe(category_data={'name': 'teste_se_entendi'})
        response = self.client.get(
            reverse('recipes:category', kwargs={'id': 1})
            )
        self.assertTemplateUsed(response, 'recipes/pages/category.html')

    def test_content_category_if_title_exists(self):
        self.make_recipe()
        response = self.client.get(
            reverse('recipes:category', kwargs={'id': 1})
            )
        content = response.content.decode()
        self.assertIn('titletest', content)

    def test_view_category_404_not_found_if_not_category(self):
         
        response = self.client.get(
            reverse('recipes:category', kwargs={'id': 1})
            )
        self.assertEqual(response.status_code, 404)

    def test_view_category_is_published_is_false_one(self):

        self.make_recipe(is_published=False)
        response = self.client.get(
            reverse('recipes:category', kwargs={'id': 1})
            )
        self.assertEqual(response.status_code, 404)

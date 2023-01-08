from django.urls import reverse, resolve
from recipes import views
from .test_base_ import TestBase


class RecipeViewRecipeTest(TestBase):

    def test_recipes_recipe_view_recipe_function_is_correct(self):

        view = resolve(reverse('recipes:recipe', kwargs={'id': 1}))
        self.assertIs(view.func, views.recipe)
    
    def recipe_detail_not_found_if_not_recipe(self):

        response = self.client.get(reverse('recipes:recipe', kwargs={'id': 1}))
        self.assertEqual(response.status_code, 404)

    def recipe_detail_status_code_ok_if_recipe(self):

        self.make_recipe()
        response = self.client.get(reverse('recipes:recipe', kwargs={'id': 1}))
        self.assertEqual(response.status_code, 200)

    def test_title_in_content_in_view_recipe_if_not_recipes(self):
        response = self.client.get(reverse('recipes:recipe', kwargs={'id': 1}))
        content = response.content.decode()

        self.assertNotIn('titletest', content)
        self.assertEqual(response.status_code, 404)

    def test_title_in_content_in_view_recipe(self):
        self.make_recipe()
        response = self.client.get(reverse('recipes:recipe', kwargs={'id': 1}))

        self.assertEqual(response.status_code, 200)

    def test_recipe_loads_template_the_correct(self):
        
        self.make_recipe()
        response = self.client.get(reverse(
            'recipes:recipe', kwargs={'id': 1})
            )
        self.assertTemplateUsed(response, 'recipes/pages/recipe-view.html')

    def test_view_recipe_detail_is_published_is_false(self):
        self.make_recipe(is_published=False)
        response = self.client.get(
            reverse(
                'recipes:recipe', kwargs={'id': 1}
                )
            )
        self.assertEqual(response.status_code, 404)

   
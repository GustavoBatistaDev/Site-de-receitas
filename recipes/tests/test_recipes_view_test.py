from django.urls import reverse, resolve
from recipes import views
from .test_base_ import TestBase
from recipes.models import Recipe


class RecipeViewsTest(TestBase):

    # tests home                                         
    def test_recipe_home_view_function_is_correct(self):

        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func, views.home)

    def test_view_home_status_code_200_ok(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)

    def test_view_home_loads_template_correct(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'recipes/pages/home.html')
    
    def test_recipe_home_template_shows_no_recipes_founds_if_not_recipes(self):
        self.make_recipe()
        Recipe.objects.get(pk=1).delete()
        response = self.client.get(reverse('recipes:home'))
        self.assertIn(
            'There are no recipes here!',
            response.content.decode('utf-8')
            )
    
    def test_recipe_home_template_loads_recipes(self):

        self.make_recipe()
        response = self.client.get(reverse('recipes:home'))
        content = response.content.decode('utf-8')
        self.assertIn('titletest', content)
    
    # end_tests_home

    # tests category
    def test_recipe_view_category_function_is_correct(self):

        view = resolve(reverse('recipes:category', kwargs={'id': 1}))
        self.assertIs(view.func, views.category)

    def test_view_category_200_ok_if_category(self):

        self.make_recipe()
        response = self.client.get(reverse('recipes:category', kwargs={'id': 1}))
        self.assertEqual(response.status_code, 200)

    def test_view_category_loads_template_correct(self):
        
        self.make_recipe()
        response = self.client.get(reverse('recipes:category', kwargs={'id': 1}))
        self.assertTemplateUsed(response, 'recipes/pages/category.html')

    def test_content_category_if_title_exists(self):
        self.make_recipe()
        response = self.client.get(reverse('recipes:category', kwargs={'id':1}))
        content = response.content.decode()
        self.assertIn('titletest', content)

    def test_view_category_404_not_found_if_not_category(self):
         
        response = self.client.get(reverse('recipes:category', kwargs={'id': 1}))
        self.assertEqual(response.status_code, 404)

    # end_tests_category

    # tests_recipe_detail
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
        content = response.content.decode()

        self.assertEqual(response.status_code, 200)

    def test_recipe_loads_template_the_correct(self):
        
        self.make_recipe()
        response = self.client.get(reverse('recipes:recipe', kwargs={'id': 1}))
        self.assertTemplateUsed(response, 'recipes/pages/recipe-view.html')
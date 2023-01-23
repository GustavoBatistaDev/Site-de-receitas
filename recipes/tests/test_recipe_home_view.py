from django.urls import reverse, resolve
from recipes import views
from .test_base_ import TestBase
from recipes.models import Recipe
from unittest.mock import patch


class RecipeViewHomeTest(TestBase):

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

    def test_recipe_home_if_is_published_is_false(self):

        # testing if is_published is correct
        self.make_recipe(is_published=False, title='not recipe match')
        response = self.client.get(reverse('recipes:home'))
        self.assertIn(
            'There are no recipes here!',
            response.content.decode('utf-8')
            )

    @patch('recipes.views.PER_PAGE', new=6)
    def test_recipe_pagination(self):
        for i in range(18):
            u = {'slug': f'r{i}', 'author_data': {'username': f'u{i}'}}
            self.make_recipe(**u)
        response = self.client.get(reverse('recipes:home'))
        recipes = response.context['recipes']
        pagination = recipes.paginator 
       
        self.assertEqual(pagination.num_pages, 3)
        self.assertEqual(len(pagination.get_page(1)), 6)
    
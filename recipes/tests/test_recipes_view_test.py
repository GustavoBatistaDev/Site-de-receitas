from django.test import TestCase
from django.urls import reverse, resolve
from recipes import views
from recipes.models import Category, Recipe
from django.contrib.auth.models import User


class RecipeViewsTest(TestCase):
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
        response = self.client.get(reverse('recipes:home'))
        self.assertIn(
            'There are no recipes here!',
            response.content.decode('utf-8')
            )

    def test_recipe_home_template_loads_recipes(self):
        category = Category.objects.create(name='Category')
        author = User.objects.create_user(
            first_name='user',
            last_name='name',
            username='username',
            password='123456',
            email='username@email.com',
        )
        recipe = Recipe.objects.create(
            category=category,
            author=author,
            title='Recipe Title',
            description='Recipe Description',
            slug='recipe-slug',
            preparation_time=10,
            preparation_time_unit='Minutos',
            servings=5,
            servings_unit='Porções',
            preparation_steps='Recipe Preparation Steps',
            preparation_steps_is_html=False,
            is_published=True,
        )

        response = self.client.get(reverse('recipes:home'))

        pass
    
    def test_recipe_view_category_function_is_correct(self):

        view = resolve(reverse('recipes:category', kwargs={'id': 1}))
        self.assertIs(view.func, views.category)

    def test_recipes_recipe_view_recipe_function_is_correct(self):

        view = resolve(reverse('recipes:recipe', kwargs={'id': 1}))
        self.assertIs(view.func, views.recipe)

    def recipe_detail_not_found_if_not_recipe(self):

        response = self.client.get(reverse('recipes:recipe', kwargs={'id': 1}))
        self.assertEqual(response.status_code, 404)

    def test_view_category_404_not_found_if_not_category(self):
        response = self.client.get(reverse('recipes:category', kwargs={'id': 1}))
        self.assertEqual(response.status_code, 404)   


from django.test import TestCase
from recipes.models import Category, Recipe
from django.contrib.auth.models import User


class TestBase(TestCase):

    def make_category(self, name: str = 'categoria_test'):
        return Category.objects.create(name=name)

    def make_author(
        self,
        first_name='Name_test',
        last_name='last_name_test',
        username='usernametest',
        password='password@test',
        email='email@test'
    ):

        return User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            password=password,
            email=email
        )

    def make_recipe(
        self,
        category_data=None,
        author_data=None,
        title='titletest',
        description='descriptiontest',
        slug='slug-test',
        preparation_time=10,
        preparation_time_unit='testminutes',
        servings=5,
        servings_unit='testservingsunit',
        preparation_steps='preparationstepstest',
        preparation_steps_is_html=False,
        is_published=True,
    ):

        if category_data is None:
            category_data = {}

        elif author_data is None:
            author_data = {}

        return Recipe.objects.create(
                category=self.make_category(**category_data),
                author=self.make_author(**author_data),
                title='titletest',
                description='descriptiontest',
                slug='slug-test',
                preparation_time=10,
                preparation_time_unit='testminutes',
                servings=5,
                servings_unit='testservingsunit',
                preparation_steps='preparationstepstest',
                preparation_steps_is_html=False,
                is_published=True,
            )
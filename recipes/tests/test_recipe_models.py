from .test_base_ import TestBase, Recipe
from django.core.exceptions import ValidationError
from parameterized import parameterized


class RecipeModelTest(TestBase):

    def setUp(self) -> None:
        self.recipe = self.make_recipe()
        return super().setUp()

    @parameterized.expand([

            ('title', 65),
            ('description', 165),
            ('preparation_time_unit', 65),
            ('servings_unit', 65),

        ])
    def test_recipes_fields_max_length(self, field, max_length):
        setattr(self.recipe, field, 's' * (max_length+1))
        with self.assertRaises(ValidationError):
            self.recipe.full_clean()
    
    def create_recipe_for_tests_coluns_default(
        self,
        title='titletest',
        description='Description',
        slug='recipe-slug',
        preparation_time_unit='Minutos',
        preparation_time=10,
        servings=5,
        servings_unit='Porções',
        preparation_steps='Recipe Preparation Steps',
    ):
        recipe = Recipe(
            category=self.make_category(name='test default category'),
            author=self.make_author(username='new user'),
            title=title,
            description=description,
            slug=slug,
            preparation_time=preparation_time,
            preparation_time_unit=preparation_time_unit,
            servings=servings,
            servings_unit=servings_unit,
            preparation_steps=preparation_steps,
        )
        recipe.full_clean()
        recipe.save()
        return recipe

    def test_recipe_preparation_steps_html_is_false_by_default(self):
        recipe = self.create_recipe_for_tests_coluns_default(
                    title='TestPreparationStepsHtml',
                    slug='teste-1'
            )

        self.assertFalse(
            recipe.preparation_steps_is_html, 
            msg='preparation_steps_is_html por default=True'
        )

    def test_recipe_is_published_default_is_true(self):
        recipe = self.create_recipe_for_tests_coluns_default(
            title='test ispublished is true',
            slug='teste-2'
         
        )

        self.assertFalse(
            recipe.is_published,
            msg='is_published for default=True'
        )
      
    def test_recipe_string_representation(self):
        title = self.recipe

        self.assertEqual(str(title), 'titletest')
      
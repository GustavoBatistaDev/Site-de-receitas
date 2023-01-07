from .test_base_ import TestBase
from django.core.exceptions import ValidationError


class RecipeModelTest(TestBase):

    def setUp(self) -> None:
        self.category = self.make_category(name='category test')
        return super().setUp()

    def test_recipe_model_category_string_representation_object(self):
        
        name_category = self.category

        self.assertEqual(str(name_category), self.category.name)

    def test_max_length_name_category_is_65_chars(self):
        self.category.name = 'A' * 66
  
        with self.assertRaises(ValidationError):
            self.category.full_clean()


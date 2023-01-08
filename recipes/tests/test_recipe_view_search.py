from django.urls import reverse, resolve
from recipes import views
from .test_base_ import TestBase


class RecipeViewSearch(TestBase):
   
    # teste_search
    def test_view_the_search_url_if_the_view_is_correct(self):
        response = resolve(reverse('recipes:search'))
        self.assertIs(response.func, views.search)
        
    def test_recipe_search_loads_correct_templates(self):
        response = self.client.get(f'{reverse("recipes:search")}?search=value')

        self.assertTemplateUsed(response, 'recipes/pages/search.html')

    def test_recipe_search_raises_404_if_not_termo(self):
        response = self.client.get(reverse('recipes:search'))

        self.assertEqual(response.status_code, 404)

    def test_recipe_search_term_is_on_title_on_page_and_escaped(self):
        self.make_recipe(title='test search one', slug='one-test')
        response = self.client.get(f'{reverse("recipes:search")}?search=value')

        self.assertIn(
            'Termo | &quot;value&quot;',
            response.content.decode()
        )

    def test_recipe_search_loads_404_if_not_termo(self):
        response = self.client.get(f'{reverse("recipes:search")}?search= ')

        self.assertEqual(response.status_code, 404)

    def test_recipe_search_query_title_is_correct(self):

        # testando search por título
        title1 = ' this title test one'
        title2 = 'this title test two'

        recipe1 = self.make_recipe(
            slug='test one', title=title1, author_data={'username': 'joao'}
            )
        recipe2 = self.make_recipe(
            slug='test two', title=title2, author_data={'username': 'alvaro'}
            )

        search_url = f'{reverse("recipes:search")}'
        response1 = self.client.get(f'{search_url}?search={title1}')
        response2 = self.client.get(f'{search_url}?search={title2}')

        response_both = self.client.get(f'{search_url}?search=this')

        self.assertIn(recipe1, response1.context['recipes'])
        self.assertNotIn(recipe1, response2.context['recipes'])

        self.assertNotIn(recipe2, response1.context['recipes'])
        self.assertIn(recipe2, response2.context['recipes'])

        self.assertIn(recipe2, response_both.context['recipes'])
        self.assertIn(recipe1, response_both.context['recipes'])

    def test_recipe_search_query_description_is_correct(self):
        # testando search por descrição

        description1 = 'this description test one'
        description2 = 'this description test two'

        recipe1 = self.make_recipe(
            slug='test-one',
            description=description1,
            author_data={'username': 'joao'},
            title='test description 1'
            )
        recipe2 = self.make_recipe(
            slug='test two',
            description=description2,
            author_data={'username': 'alvaro'},
            title='test description 2'
            )

        search_url = f'{reverse("recipes:search")}'
        response1 = self.client.get(f'{search_url}?search={description1}')
        response2 = self.client.get(f'{search_url}?search={description2}')

        response_both = self.client.get(f'{search_url}?search=this')

        self.assertIn(recipe1, response1.context['recipes'])
        self.assertNotIn(recipe1, response2.context['recipes'])

        self.assertNotIn(recipe2, response1.context['recipes'])
        self.assertIn(recipe2, response2.context['recipes'])

        self.assertIn(recipe2, response_both.context['recipes'])
        self.assertIn(recipe1, response_both.context['recipes'])




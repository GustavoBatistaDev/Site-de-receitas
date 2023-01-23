from unittest import TestCase
from pagination import make_pagination_range
from recipes.tests.test_base_ import TestBase
from django.urls import reverse, resolve


class PaginationTest(TestCase):
    def test_make_pagination_range_return_a_pagination_range(self):
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=1
        )['pagination']

        self.assertEqual([1, 2, 3, 4], pagination)

    def test_first_range_is_static(self):
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=2
        )['pagination']

        self.assertEqual([1, 2, 3, 4], pagination)

        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=3
        )['pagination']

        self.assertEqual([2, 3, 4, 5], pagination)

        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=4
        )['pagination']

        self.assertEqual([3, 4, 5, 6], pagination)
    # duplicado

    def test_make_sure_middle_ranges_are_correct(self):
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=10
        )['pagination']

        self.assertEqual([9, 10, 11, 12], pagination)

        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=15  
        )['pagination']

        self.assertEqual([14, 15, 16, 17], pagination)

        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=19
        )['pagination']

        self.assertEqual([17, 18, 19, 20], pagination)

    def test_make_pagination_range_end(self):
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=18
        )['pagination']

        self.assertEqual([17, 18, 19, 20], pagination)

        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=19
        )['pagination']

        self.assertEqual([17, 18, 19, 20], pagination)

        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=20
        )['pagination']

        self.assertEqual([17, 18, 19, 20], pagination)

        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=21
        )['pagination']

        self.assertEqual([17, 18, 19, 20], pagination)


class TestPaginationCorrect(TestBase):
    def setUp(self):
        
        self.make_recipe(
            title='recipe1', slug='recipe-slug-1', author_data={'username': 'gustav1'}  # noqa: E501
        )

        self.make_recipe(
            title='recipe2', slug='recipe-slug-2', author_data={'username': 'gustav2'}  # noqa: E501

        )
        self.make_recipe(
            title='recipe3', slug='recipe-slug-3', author_data={'username': 'gustav3'}  # noqa: E501

        )

        return super().setUp()

    def test_pages_in_view_home(self):
        response = self.client.get(f'{reverse("recipes:home")}?page=1')  # noqa: E501       
        content = response.content.decode('utf-8')
        self.assertNotIn('recipe1', content)

    def test_pages_in_view_search(self):
        response = self.client.get(f'{reverse("recipes:search")}?page=1&search=e')  # noqa: E501       
        content = response.content.decode('utf-8')
        self.assertNotIn('recipe1', content)

    # escrever o teste em que testa se a paginacao da view categoria esta funcionando
    def test_pages_in_view_category(self):
        ...












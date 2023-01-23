from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.http import HttpResponse, HttpRequest
from .models import Recipe
from django.http import Http404
from django.db.models import Q
from utils.pagination import make_pagination
from django.http import QueryDict
import os
from django.contrib import messages
from django.contrib.messages import constants


PER_PAGE = os.environ.get('PER_PAGE', '2')


def home(request: HttpRequest) -> HttpResponse:
    recipes: QueryDict = Recipe.objects.filter(is_published=True).order_by('-id')  # noqa: E501
    
    page_obj, pagination_range = make_pagination(
            request=request,
            query_set=recipes,
            per_page=PER_PAGE,
            qty_pages=4
    )

    return render(
        request, 'recipes/pages/home.html', context={'recipes': page_obj, 'pagination_range': pagination_range}  # noqa: E501
        )


def recipe(request: HttpRequest, id: int) -> HttpResponse:
    recipe: Recipe = get_object_or_404(Recipe, id=id, is_published=True)
    return render(request, 'recipes/pages/recipe-view.html', context={
            'recipe': recipe,
            'is_detail_page': True
            })


def category(request: HttpRequest, id: int) -> HttpResponse:

    recipes: list = get_list_or_404(Recipe.objects.filter(
            is_published=True,
            category__id=id).order_by('-id'),
            )

    category_name = recipes[0].category.name
    page_obj, pagination_range = make_pagination(
        request=request,
        query_set=recipes,
        per_page=PER_PAGE,
        qty_pages=4

    )
    
    return render(
        request, 'recipes/pages/category.html', context={
                'recipes': page_obj,
                'pagination_range': pagination_range,
                'category': category_name,
                })


def search(request: HttpRequest) -> HttpResponse:  
    search_termo = request.GET.get('search', '').strip()

    if not search_termo:
        raise Http404()

    recipes: QueryDict = Recipe.objects.filter(
        Q(
            Q(title__icontains=search_termo) |
            Q(description__icontains=search_termo),
            is_published=True
        )
    ).order_by('-id')

    page_obj, pagination_range = make_pagination(
        request=request,
        query_set=recipes,
        per_page=PER_PAGE,
        qty_pages=4

    )
    print(str(page_obj))

    return render(
        request, 'recipes/pages/search.html', {
            'page_title': f'Termo | "{search_termo}"',
            'recipes': page_obj,
            'pagination_range': pagination_range,
            'adittional_url_query': f'&search={search_termo}'
        }
    )
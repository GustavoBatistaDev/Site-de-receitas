from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.http import HttpResponse, HttpRequest
from .models import Recipe
from django.http import Http404
from django.db.models import Q
from django.core.paginator import Paginator


def home(request: HttpRequest) -> HttpResponse:
    recipes = Recipe.objects.filter(is_published=True).order_by('-id')

    current_page = request.GET.get('page', 1)
    paginator = Paginator(recipes, 1)
    page_obj = paginator.get_page(current_page)

    return render(
        request, 'recipes/pages/home.html', context={'recipes': page_obj}
        )


def recipe(request: HttpRequest, id: int) -> HttpResponse:
    recipe = get_object_or_404(Recipe, id=id, is_published=True)
    return render(request, 'recipes/pages/recipe-view.html', context={
            'recipe': recipe,
            'is_detail_page': True
            })


def category(request: HttpRequest, id: int) -> HttpResponse:

    recipes = get_list_or_404(Recipe.objects.filter(
            is_published=True,
            category__id=id).order_by('-id'),
            )

    category_name = recipes[0].category.name
    
    return render(
        request, 'recipes/pages/category.html', context={
                'recipes': recipes,
                'category': category_name,
                })


def search(request: HttpRequest) -> HttpResponse:  
    search_termo = request.GET.get('search', '').strip()

    if not search_termo:
        raise Http404()

    recipes = Recipe.objects.filter(
        Q(
            Q(title__icontains=search_termo) |
            Q(description__icontains=search_termo),
            is_published=True
        )
    ).order_by('-id')

    return render(
        request, 'recipes/pages/search.html',

        {'page_title': f'Termo | "{search_termo}"', 'recipes': recipes}
        )
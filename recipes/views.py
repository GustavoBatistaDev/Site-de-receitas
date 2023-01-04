from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.http import HttpResponse, HttpRequest
from utils.recipes.factory import make_recipe
from .models import Recipe
from django.http import Http404




def home(request: HttpRequest) -> HttpResponse:
    recipes = Recipe.objects.filter(is_published=True).order_by('-id')
    return render(request, 'recipes/pages/home.html', context={'recipes': recipes})



def recipe(request: HttpRequest, id: int) -> HttpResponse:
    recipe = get_object_or_404(Recipe,id=id, is_published=True)
    return render(request, 'recipes/pages/recipe-view.html', context={
            'recipe': recipe,
            'is_detail_page':True
            })

def category(request: HttpRequest, id: int) -> HttpResponse:

    recipes = get_list_or_404(Recipe.objects.filter(
            is_published=True,
            category__id=id).order_by('-id'),
            )

    category_name = recipes[0].category.name
    

    return render(request, 'recipes/pages/category.html', context={'recipes': recipes, 'category':category_name})
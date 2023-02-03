from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.http import HttpResponse, HttpRequest
from .models import Recipe
from django.http import Http404
from django.db.models import Q
from utils.pagination import make_pagination
from django.http import QueryDict
import os
from django.views.generic.list import ListView
from django.http import JsonResponse
from django.forms.models import model_to_dict
from tag.models import Tag

PER_PAGE = '2'


class RecipeListViewBase(ListView):
    model = Recipe
    context_object_name = 'recipes'
    paginate_by = None
    ordering = ['-id']
    template_name = 'recipes/pages/home.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(is_published=True)
        qs = qs.select_related('author', 'category')
        return qs
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        page_obj, pagination_range = make_pagination(
            request=self.request,
            query_set=context.get('recipes'),
            per_page=PER_PAGE,
            qty_pages=4
 
        )
        context.update(
            {'recipes': page_obj,
             'pagination_range': pagination_range}
            )
        return context
    

class Home(RecipeListViewBase):
    template_name = 'recipes/pages/home.html'


def home(request: HttpRequest) -> HttpResponse:
    recipes: QueryDict = Recipe.objects.filter(is_published=True).order_by('-id').select_related('category', 'author')  # noqa: E501
    
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

    return render(
        request, 'recipes/pages/search.html', {
            'page_title': f'Termo | "{search_termo}"',
            'recipes': page_obj,
            'pagination_range': pagination_range,
            'adittional_url_query': f'&search={search_termo}'
        }
    )


# views que retornam JSON!!!!

class RecipeListViewApi(RecipeListViewBase):
    template_name = 'recipes/pages/home.html'

    def render_to_response(self, context, **response_kwargs):
        recipes = self.get_context_data()['recipes']
        recipes_dict = recipes.object_list.values()

        print(recipes_dict)
        return JsonResponse(list(recipes_dict), safe=False)


def home_api(request: HttpRequest) -> HttpResponse:
    recipes = Recipe.objects.filter(is_published=True).order_by('-id').values()  # noqa: E501
    return JsonResponse(list(recipes), safe=False)


def detail_api(request: HttpRequest, id: int) -> HttpResponse:
    recipe = get_object_or_404(Recipe, id=id)
    recipe_dict = model_to_dict(recipe)

    if recipe_dict.get('cover'):
        recipe_dict['cover'] = request.build_absolute_uri() + recipe_dict['cover'].url[1:]
    else:
        recipe_dict['cover'] = ''

    del recipe_dict['is_published']
    return JsonResponse(recipe_dict)


def theory(request, *args, **kwargs):
    return render(
        request, 
        'recipes/pages/theory.html'
        )

#  tag


class RecipeListViewTag(RecipeListViewBase):
    template_name = 'recipes/pages/tag.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(tags__slug=self.kwargs.get('slug', ''))
        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        page_title = Tag.objects.filter(
            slug=self.kwargs.get('slug', '')
        ).first()

        if not page_title:
            page_title = 'No recipes found'

        page_title = f'{page_title} - Tag |'

        ctx.update({
            'page_title': page_title,
        })

        return ctx

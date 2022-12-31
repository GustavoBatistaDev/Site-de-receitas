from django.shortcuts import render
from django.http import HttpResponse, HttpRequest


def home(request: HttpRequest) -> HttpResponse:
    return render(request, 'recipes/pages/home.html')

def recipe(request: HttpRequest, id: int) -> HttpResponse:
    return render(request, 'recipes/pages/recipe-view.html')
from django.urls import path
from . import views


app_name = 'recipes'

urlpatterns = [
    path('recipes/search/', views.search, name='search'),
    path('', views.Home.as_view(), name='home'),
    path('recipes/<int:id>/', views.recipe, name='recipe'),
    path('recipes/category/<int:id>/', views.category, name='category'),

    
]

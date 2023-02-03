from django.urls import path
from . import views


app_name = 'recipes'

urlpatterns = [
    path('recipes/search/', views.search, name='search'),
    path('recipes/tags/<slug:slug>', views.RecipeListViewTag.as_view(), name='tag'),
    path('', views.home, name='home'),
    path('recipes/<int:id>/', views.recipe, name='recipe'),
    path('recipes/category/<int:id>/', views.category, name='category'),
    path('recipes/api/v1/', views.home_api, name='recipe_api_v1'),
    path('recipes/api/v1/<int:id>/', views.detail_api, name='recipe_api_v1'),
    path('recipes/theory/', views.theory, name='theory')

]

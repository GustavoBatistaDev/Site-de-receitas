from django.urls import path
from . import views


app_name = 'authors'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('register/create/', views.register_create, name='create'),
    path('login/', views.login_view, name='login_view'),
    path('login/create/', views.login_create, name='login_create'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/<int:id>/edit/', views.DashBoardRecipeEdit.as_view(), name='dashboard_recipe_edit'),  # noqa
    path(
        'dashboard/create/',
        views.DashBoardRecipeCreate.as_view(),
        name='dashboard_create'
    ),
    path(
        'dashboard/<int:id>/delete/',
        views.DashboardRecipeDelete.as_view(),
        name='dashboard_recipe_delete'
    ),
    path(
        'profile/<int:id>/',
        views.profile_view,
        name='profile'
    ),
    
]
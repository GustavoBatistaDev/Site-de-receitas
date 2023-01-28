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
    path('dashboard/<int:id>/edit/', views.dashboard_recipe_edit, name='dashboard_recipe_edit'),  # noqa
    path(
        'dashboard/create/',
        views.dashboard_create_recipe,
        name='dashboard_create'
    )
]

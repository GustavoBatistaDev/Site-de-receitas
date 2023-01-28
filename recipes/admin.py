from django.contrib import admin
from .models import Category, Recipe


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug', 'created_at', 'is_published', 'author')  # noqa
    list_editable = ('is_published',)
    list_display_links = 'id', 'title', 'slug'
    search_fields = 'title', 'id', 'description', 'slug', 'preparation_steps'
    list_filter = 'category', "author", 'is_published', 'preparation_steps_is_html'
    ordering = '-id',
    prepopulated_fields = {
        'slug': ('title',)
    }



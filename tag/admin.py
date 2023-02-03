from django.contrib import admin
from .models import Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    list_display_links = ('id', 'slug')
    list_editable = ('name', )
    prepopulated_fields = {
        'slug': ('name',)
    }


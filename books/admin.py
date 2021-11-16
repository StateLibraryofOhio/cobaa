from django.contrib import admin

from .models import *


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name', ]
    search_fields = ['name', ]


@admin.register(Award)
class AwardAdmin(admin.ModelAdmin):

    def title(self, obj):
        return obj.get_short_book_title

    def authors(self, obj):
        return obj.get_authors

    list_display = ['__str__', 'title', 'authors']
    list_filter = ['award', 'year', 'prize']
    search_fields = ['award', 'book__title', 'year', 'prize']
    ordering = ['award', '-year', 'book__title']


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    search_fields = ['title']
    filter_horizontal = ('authors', 'tags')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    search_fields = ['tag']


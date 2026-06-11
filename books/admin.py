from django.contrib import admin
from django.utils import timezone
from .models import *


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name', ]
    search_fields = ['name', ]


@admin.register(Award)
class AwardAdmin(admin.ModelAdmin):

    def get_changeform_initial_data(self, request):
        initial = {}

        # Prefer explicit GET params (useful if you redirect with query params)
        award = request.GET.get('award')
        year = request.GET.get('year')

        if award:
            initial['award'] = award
        else:
            # fallback to last saved value in session
            last_award = request.session.get('last_award')
            if last_award:
                initial['award'] = last_award

        if year:
            initial['year'] = year
        else:
            last_year = request.session.get('last_award_year')
            if last_year:
                initial['year'] = last_year
            else:
                initial['year'] = timezone.now().year

        return initial

    def response_add(self, request, obj, post_url_continue=None):
        # Save the chosen award/year in the user's session for next time.
        # obj.award is the stored choice value (e.g. 'c', 't', etc.)
        request.session['last_award'] = obj.award
        request.session['last_award_year'] = str(obj.year)
        request.session.modified = True

        return super().response_add(request, obj, post_url_continue=post_url_continue)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    search_fields = ['title']
    filter_horizontal = ('authors', 'tags')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    search_fields = ['tag']

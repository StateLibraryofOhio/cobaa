from django.contrib.postgres.search import SearchQuery, SearchVector
from django_filters import BooleanFilter, CharFilter, ChoiceFilter, FilterSet

from .models import Award, Book


class BookFilter(FilterSet):

    @staticmethod
    def filter_by_year(queryset, name, value):
        return queryset.filter(awards__year=value)

    # Collect all unique years from the database, ordered in descending order
    YEARS = [(year, year) for year in Award.objects.values_list('year', flat=True).distinct().order_by('-year')]

    award_year = ChoiceFilter(field_name='award_year', method='filter_by_year',
                              label='Award Year', choices=YEARS, empty_label="All Years")

    @staticmethod
    def filter_by_keyword(queryset, name, value):
        query = SearchQuery(value, config="english")
        vector = SearchVector('title', 'authors__name', 'tags__tag', config="english")
        return queryset.annotate(search=vector).filter(search=query).distinct('title')

    @staticmethod
    def filter_winners_only(queryset, name, value):
        return queryset.filter(awards__prize="w")

    awards__award = ChoiceFilter(choices=Award._meta.get_field('award').choices, label='Award')
    keywords = CharFilter(method='filter_by_keyword', label='Title, Author, or Keywords')
    winner = BooleanFilter(field_name='prize', method='filter_winners_only', label='Winner')

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)

        if self.form.cleaned_data.get('awards__award') and self.form.cleaned_data.get('award_year'):
            queryset = queryset.filter(awards__award=self.form.cleaned_data.get('awards__award'),
                                       awards__year=self.form.cleaned_data.get('award_year'))

        return queryset

    class Meta:
        model = Book
        fields = ['awards__award', 'keywords', 'winner', 'award_year']

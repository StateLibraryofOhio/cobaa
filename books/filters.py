from django.contrib.postgres.search import SearchQuery, SearchVector
from django_filters import BooleanFilter, CharFilter, ChoiceFilter, FilterSet

from .models import Award, Book


class BookFilter(FilterSet):

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

    class Meta:
        model = Book
        fields = ['awards__award', 'keywords', 'winner']

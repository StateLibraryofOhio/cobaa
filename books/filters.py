from django.db import connection
from django_filters import BooleanFilter, CharFilter, ChoiceFilter, FilterSet

from .models import Award, Book

STOP_WORDS = {'and', 'or', 'the', 'a', 'an', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}


class BookFilter(FilterSet):
    @staticmethod
    def filter_by_year(queryset, name, value):
        return queryset.filter(awards__year=value)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set choices dynamically when filter is instantiated
        try:
            years = [(year, year) for year in Award.objects.values_list('year', flat=True).distinct().order_by('-year')]
            self.filters['award_year'].field.choices = [('', 'All Years')] + years
        except:
            # If database doesn't exist yet, use empty choices
            self.filters['award_year'].field.choices = [('', 'All Years')]

    award_year = ChoiceFilter(field_name='award_year', method='filter_by_year',
                              label='Award Year', choices=[('', 'All Years')], empty_label=None)

    @staticmethod
    def filter_by_keyword(queryset, name, value):
        if not value.strip():
            return queryset

        try:
            with connection.cursor() as cursor:
                terms = value.strip().split()
                # Remove stop words
                filtered_terms = [term for term in terms if term.lower() not in STOP_WORDS]

                if not filtered_terms:
                    return queryset

                # If user entered 2+ meaningful terms, use AND logic
                # If only 1 term, just search for that term
                if len(filtered_terms) > 1:
                    escaped_terms = [term.replace('"', '""') for term in filtered_terms]
                    fts_query = ' AND '.join(escaped_terms)  # "black AND white"
                else:
                    fts_query = filtered_terms[0].replace('"', '""')

                # Use named parameters to avoid formatting issues
                cursor.execute("""
                               SELECT bb.id
                               FROM books_book bb
                                        JOIN book_search bs ON bb.id = bs.rowid
                               WHERE book_search MATCH :search_term
                               """, {'search_term': fts_query})

                book_ids = [row[0] for row in cursor.fetchall()]

            return queryset.filter(id__in=book_ids) if book_ids else queryset.none()

        except Exception as e:
            # Fallback to no filtering if search fails
            print(f"Search error: {e}")
            return queryset

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
        # fields = ['awards__award', 'keywords', 'winner', 'award_year']
        fields = ['awards__award', 'keywords', 'winner']

from django.views.generic.list import ListView

from cart.forms import CartAddBookForm
from .filters import BookFilter
from .models import Award, Book


class AwardListView(ListView):
    model = Award
    template_name = 'awards/award_list.html'

    paginate_by = 20

    def get_queryset(self):
        queryset = Award.objects.all().filter(hidden=0).order_by('award', '-year', 'book__title')

        return queryset


class BookListView(ListView):
    model = Book
    template_name = 'books/book_list.html'

    paginate_by = 20

    def get_queryset(self):
        queryset = Book.published.all().order_by('title').distinct()
        filtered_list = BookFilter(self.request.GET, queryset=queryset)

        return filtered_list.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = BookFilter(self.request.GET, queryset=self.get_queryset())
        context['cart_form'] = CartAddBookForm()

        return context

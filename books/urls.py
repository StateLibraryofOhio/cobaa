from django.urls import path

from .views import AwardListView, BookListView

app_name = 'books'

urlpatterns = [
    path('', BookListView.as_view(), name='book_list'),
    path('books/', BookListView.as_view(), name='book_list'),
    path('awards/', AwardListView.as_view(), name='award_list'),
    ]

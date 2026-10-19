from django.urls import path

from .views import BookListView

app_name = 'books'

urlpatterns = [
    path('', BookListView.as_view(), name='book_list'),
    path('books/', BookListView.as_view(), name='book_list'),
    ]

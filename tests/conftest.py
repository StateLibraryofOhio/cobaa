import pytest
from django.db import connection

from books.models import Author, Award, Book


@pytest.fixture(autouse=True)
def fts_table(django_db_setup, django_db_blocker):
    """book_search (FTS5) is created outside migrations in production; create it for tests."""
    with django_db_blocker.unblock(), connection.cursor() as cursor:
        cursor.execute("CREATE VIRTUAL TABLE IF NOT EXISTS book_search USING fts5(combined_text)")


@pytest.fixture
def book(db):
    b = Book.objects.create(title='The Great Test Book')
    b.authors.add(Author.objects.create(name='Jane Author'))
    Award.objects.create(award='o', year=2020, prize='w', book=b)
    return b


@pytest.fixture
def hidden_book(db):
    return Book.objects.create(title='Secret Book', hidden=True)

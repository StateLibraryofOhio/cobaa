import pytest
from django.urls import reverse


@pytest.mark.parametrize('name', [
    'books:book_list',
    'cart:cart_detail',
    'about',
])
def test_public_pages_ok(client, db, name):
    assert client.get(reverse(name)).status_code == 200


def test_book_list_hides_hidden(client, book, hidden_book):
    content = client.get(reverse('books:book_list')).content.decode()
    assert book.title in content
    assert hidden_book.title not in content


def test_keyword_search_matches_title_and_author(client, book, hidden_book):
    url = reverse('books:book_list')
    assert book.title in client.get(url, {'keywords': 'Great'}).content.decode()
    assert book.title in client.get(url, {'keywords': 'Jane'}).content.decode()
    assert book.title not in client.get(url, {'keywords': 'zzzznomatch'}).content.decode()

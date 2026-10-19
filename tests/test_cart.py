from django.urls import reverse

from orders.models import Order, OrderItem


def add(client, book, quantity=1):
    return client.post(reverse('cart:cart_add', args=[book.id]),
                       {'quantity': quantity}, HTTP_REFERER='http://testserver/')


def cart_of(client):
    return client.session.get('cart', {})


def test_add_to_cart(client, book):
    assert add(client, book, 2).status_code == 302
    assert cart_of(client)[str(book.id)]['quantity'] == 2


def test_add_accumulates(client, book):
    add(client, book, 2)
    add(client, book, 3)
    assert cart_of(client)[str(book.id)]['quantity'] == 5


def test_add_invalid_quantity_ignored(client, book):
    add(client, book, 0)
    assert cart_of(client) == {}


def test_add_rejects_foreign_referer(client, book):
    r = client.post(reverse('cart:cart_add', args=[book.id]), {'quantity': 1},
                    HTTP_REFERER='http://evil.example/')
    assert r.status_code == 400


def test_add_requires_post(client, book):
    assert client.get(reverse('cart:cart_add', args=[book.id])).status_code == 405


def test_add_unknown_book_404(client, db):
    assert client.post(reverse('cart:cart_add', args=[999]), {'quantity': 1}).status_code == 404


def test_update_overrides_quantity(client, book):
    add(client, book, 5)
    client.post(reverse('cart:cart_update', args=[book.id]), {'quantity': 2, 'override': 'on'})
    assert cart_of(client)[str(book.id)]['quantity'] == 2


def test_remove(client, book):
    add(client, book)
    client.post(reverse('cart:cart_remove', args=[book.id]))
    assert cart_of(client) == {}


def test_clear(client, book):
    add(client, book)
    client.post(reverse('cart:cart_clear'))
    assert cart_of(client) == {}


def test_export_csv(client, book):
    add(client, book, 3)
    r = client.get(reverse('cart:cart_export'))
    assert r['Content-Type'].startswith('text/csv')
    body = r.content.decode()
    assert 'title,authors,awards,quantity' in body
    assert 'The Great Test Book' in body and 'Jane Author' in body


def test_retrieve_unknown_code(client, db):
    r = client.post(reverse('cart:cart_retrieve'), {'order_id': 'NOPE00'})
    assert r.status_code == 302 and r.url == reverse('books:book_list')


def test_retrieve_existing_order(client, book):
    order = Order.objects.create(id='ABC123', inst_name='Lib', amount_requested=10)
    OrderItem.objects.create(order=order, book=book, quantity=4)
    r = client.post(reverse('cart:cart_retrieve'), {'order_id': 'ABC123'})
    assert r.url == reverse('cart:cart_detail')
    assert cart_of(client)[str(book.id)]['quantity'] == 4

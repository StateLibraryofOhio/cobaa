from django.conf import settings

from books.models import Book


class Cart(object):

    def __init__(self, request):
        """
        Initialise the cart.

        :param request
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, book, quantity=1, override_quantity=False):
        """
        Add a book to the cart or update its quantity.

        :param book:
        :param quantity:
        :param override_quantity:
        :return:
        """
        # JSON only allows str keys, so convert it
        book_id = str(book.id)

        if book_id not in self.cart:
            self.cart[book_id] = {'quantity': 0}
        if override_quantity:
            self.cart[book_id]['quantity'] = quantity
        else:
            self.cart[book_id]['quantity'] += quantity
        self.save()

    def clear(self):
        # remove cart from session
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def remove(self, book):
        """
        Remove a book from the cart.
        :return:
        """
        book_id = str(book.id)
        if book_id in self.cart:
            del self.cart[book_id]
            self.save()

    def retrieve(self, order):
        """
        Re-populate cart with titles from a previous order.
        :param order:
        :return:
        """
        for item in order.items.all():
            book_id = str(item.book_id)
            quantity = item.quantity

            if book_id not in self.cart:
                self.cart[book_id] = {'quantity': quantity}
            self.save()

    def save(self):
        # mark the session as "modified" to make sure it gets saved
        self.session.modified = True

    def __iter__(self):
        """
        Iterate over items in cart and get the books from the database.
        :return:
        """
        book_ids = self.cart.keys()
        books = Book.objects.filter(id__in=book_ids)

        cart = self.cart.copy()
        for book in books:
            cart[str(book.id)]['book'] = book

        for item in cart.values():
            yield item

    def __len__(self):
        """
        Count all items in cart.
        :return:
        """
        return sum(item['quantity'] for item in self.cart.values())

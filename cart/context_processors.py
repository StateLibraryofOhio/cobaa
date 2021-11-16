from orders.forms import OrderRetrieveForm
from .cart import Cart


def cart(request):
    return {'cart': Cart(request)}


def saved_list(request):
    return {'saved_list': OrderRetrieveForm}

from cart.cart import Cart
from .forms import OrderCreateForm
from .models import Order, OrderItem
from django.utils.crypto import get_random_string


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.id = get_random_string(length=6).upper()
            # ugly way to avoid multiple submissions and primary key error
            if Order.objects.filter(pk=order.id).exists():
                order.id = get_random_string(length=6).upper()
            form.save()
            for item in cart:
                OrderItem.objects.create(order=order, book=item['book'], quantity=item['quantity'])
            return order

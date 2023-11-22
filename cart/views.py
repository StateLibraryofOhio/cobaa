import csv
from urllib.parse import urlparse

from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from django.http import HttpResponseBadRequest

from books.models import Book
from orders.forms import OrderCreateForm
from orders.models import Order
from .cart import Cart
from .forms import CartAddBookForm


def is_same_host(url, request):
    # Extract the host from the URL
    parsed_url = urlparse(url)
    redirect_host = parsed_url.netloc

    # Extract the host from the current request
    current_host = request.get_host()

    # Compare the hosts
    return redirect_host == current_host


@require_POST
def cart_add(request, book_id):
    cart = Cart(request)
    book = get_object_or_404(Book, id=book_id)
    form = CartAddBookForm(request.POST)

    if form.is_valid():
        cd = form.cleaned_data
        cart.add(book=book, quantity=cd['quantity'], override_quantity=cd['override'])
        message = "<em>" + book.title[:27] + '...</em> added.'
        messages.add_message(request, messages.SUCCESS, message=message)

    if request.headers.get('HX-Request', False):
        response = render(request, "toast.html")
        response['HX-Trigger'] = 'updateTotal'
        return response

    # Hack to keep book query filter query params intact after POST
    previous_url = request.META.get('HTTP_REFERER', 'books:book_list')

    # Check if the previous URL is from the same host
    if not is_same_host(previous_url, request):
        return HttpResponseBadRequest("Invalid redirect URL")

    return redirect(previous_url)


@require_POST
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    message = 'Your selection list has been cleared.'
    messages.add_message(request, messages.SUCCESS, message=message)

    return redirect('books:book_list')


def cart_detail(request):
    cart = Cart(request)
    order = OrderCreateForm

    for item in cart:
        item['update_quantity_form'] = CartAddBookForm(initial={'quantity': item['quantity'], 'override': True})

    return render(request, 'cart/detail.html', {'cart': cart, 'order': order})


def cart_export(request):
    cart = Cart(request)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=COBAA-Selections.csv'
    writer = csv.writer(response)
    # write header
    writer.writerow(['title', 'authors', 'awards', 'quantity'])
    # write rows
    for item in cart:
        book = item['book']
        authors = ';'.join([author.name for author in book.authors.all()])
        awards = ';'.join([str(award) for award in book.awards.all()])
        writer.writerow([book.title, authors, awards, item['quantity']])
    return response


@require_POST
def cart_remove(request, book_id):
    cart = Cart(request)
    book = get_object_or_404(Book, id=book_id)
    cart.remove(book)

    if request.headers.get('HX-Request', False):
        response = HttpResponse('')
        response['HX-Trigger'] = 'updateTotal'
        return response

    return redirect('cart:cart_detail')


@require_POST
def cart_retrieve(request):
    # clear the cart
    request.session.flush()
    cart = Cart(request)

    try:
        order_id = request.POST.get('order_id', None)
        previous_order = Order.objects.get(id=order_id)
        cart.retrieve(previous_order)
        message = str(previous_order.items.count()) + ' titles retrieved.'
        messages.add_message(request, messages.SUCCESS, message=message)
        return redirect('cart:cart_detail')
    except Order.DoesNotExist:
        message = 'Code not recognized. Please try again.'
        messages.add_message(request, messages.ERROR, message=message)
        return redirect('books:book_list')


def cart_total(request):
    # return current total items
    cart = Cart(request)
    return render(request, "total.html")


@require_POST
def cart_update(request, book_id):
    cart = Cart(request)
    book = get_object_or_404(Book, id=book_id)
    form = CartAddBookForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(book=book,
                 quantity=cd['quantity'],
                 override_quantity=cd['override'])

        message = "<em>" + book.title[:27] + '...</em> updated.'
        messages.add_message(request, messages.SUCCESS, message=message)

        if request.headers.get('HX-Request', False):
            response = render(request, "toast.html")
            response['HX-Trigger'] = 'updateTotal'
            return response

    return redirect('cart:cart_detail')

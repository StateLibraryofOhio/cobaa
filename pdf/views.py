from django.contrib import messages
from django.http import HttpResponse

from cart.cart import Cart
from orders.utils import order_create
from .services import build_accessible_pdf


def books_to_pdf(request):
    cart = Cart(request)
    order = order_create(request)
    if order:
        context = {'cart': cart, 'order': order}
        pdf_bytes = build_accessible_pdf(
            template_name='pdf/pdf.html',
            context=context,
            request=request,
        )
        response = HttpResponse(pdf_bytes, content_type='application/pdf')
        response['Content-Disposition'] = f'filename={order.inst_name} COBAA Selections.pdf'
        response['Content-Transfer-Encoding'] = 'binary'
        return response
    else:
        message = 'Oops... Something went wrong.'
        messages.add_message(request, messages.ERROR, message=message)

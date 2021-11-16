from django.contrib import messages
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

from cart.cart import Cart
from orders.utils import order_create


def books_to_pdf(request):
    cart = Cart(request)
    order = order_create(request)
    if order:
        context = {'cart': cart, 'order': order}
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'filename={order.inst_name} COBAA Selections.pdf'
        response['Content-Transfer-Encoding'] = 'binary'
        template = get_template('pdf/pdf.html')
        html = template.render(context)
        pisa_status = pisa.CreatePDF(html, dest=response)
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        return response
    else:
        message = 'Oops... Something went wrong.'
        messages.add_message(request, messages.ERROR, message=message)

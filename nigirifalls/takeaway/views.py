from django.shortcuts import render, reverse, get_object_or_404
from django.views import generic
from django.conf import settings
from io import BytesIO
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.template.loader import render_to_string
from .models import Dish, OrderInfo, OrderItem
from .forms import OrderCreateForm
from cart.forms import CartAddDishForm
from cart.cart import Cart
import weasyprint


class IndexView(generic.ListView):
    template_name = 'takeaway/index.html'

    def get_queryset(self):
        return Dish.objects.order_by('dish_type')

    def get_context_data(self):
        context = super().get_context_data()
        context['add_dish_form'] = CartAddDishForm()
        context['cart'] = Cart(self.request)
        return context


class ThankYouView(generic.DetailView):
    model = OrderInfo
    template_name = 'takeaway/thankyou.html'


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         dish=item['dish'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            cart.clear()

            # Create order confirmation email
            subject = 'Nigiri Falls - Order no. {}'.format(order.id)
            message = 'Please find attached the order confirmation for your recent order.'
            email = EmailMessage(subject,
                                 message,
                                 'nigirifalls@gmail.com',
                                 [order.email])
            # Generate PDF
            html = render_to_string('takeaway/order/order_create_pdf.html',
                                    {'order': order})
            out = BytesIO()
            weasyprint.HTML(string=html).write_pdf(
                out, stylesheets=[weasyprint.CSS(
                    settings.STATIC_ROOT + '/takeaway/pdf_style.css'
                    )]
                )
            
            # Attach email
            email.attach('order_{}.pdf'.format(order.id),
                         out.getvalue(),
                         'application/pdf')
            # Send email
            email.send()
            return render(request, 'takeaway/thankyou.html',
                          {'order': order})
    else:
        form = OrderCreateForm()
    return render(request, 'takeaway/checkout.html',
                  {'cart': cart, 'form': form})


def create_order_pdf(request, order_id):
    order = get_object_or_404(OrderInfo, id=order_id)
    html = render_to_string('takeaway/order/order_create_pdf.html',
                            {'order': order})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename=order_{}.pdf"'.format(order.id)
    weasyprint.HTML(string=html).write_pdf(
        response, stylesheets=[weasyprint.CSS(
            settings.STATIC_ROOT + 'takeaway/pdf_style.css'
        )]
    )
    return response

from django.shortcuts import render, reverse, get_object_or_404
from django.views import generic
from django.conf import settings
from django.http import HttpResponse
from .models import Dish, OrderInfo, OrderItem
from .forms import OrderCreateForm
from .mail import send_order_email_with_pdf
from cart.forms import CartAddDishForm
from cart.cart import Cart


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

            send_order_email_with_pdf(
                order,
                "Please find attached the order confirmation for your recent order.\n\nSincerely,\nThe Nigiri Falls team")

            return render(request, 'takeaway/thankyou.html',
                          {'order': order})
    else:
        form = OrderCreateForm()
    return render(request, 'takeaway/checkout.html',
                  {'cart': cart, 'form': form})

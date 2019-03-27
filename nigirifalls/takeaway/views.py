from django.shortcuts import render, reverse
from django.views import generic
from .models import Dish, OrderInfo, OrderItem
from .forms import OrderCreateForm
from cart.forms import CartAddDishForm
from cart.cart import Cart
from watson import search as watson


class IndexView(generic.ListView):
    template_name = 'takeaway/index.html'

    def get_queryset(self):
        return Dish.objects.order_by('dish_type')

    def get_context_data(self):
        context = super().get_context_data()
        context['add_dish_form'] = CartAddDishForm()
        context['cart'] = Cart(self.request)
        context['is_search'] = False
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
            return render(request, 'takeaway/thankyou.html',
                          {'order': order})
    else:
        form = OrderCreateForm()
    return render(request, 'takeaway/checkout.html',
                  {'cart': cart, 'form': form})

class SearchView(generic.ListView):       
    template_name = 'takeaway/index.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['add_dish_form'] = CartAddDishForm()
        context['cart'] = Cart(self.request)
        context['is_search'] = True
        search_results = watson.filter(Dish, "q")
        return context









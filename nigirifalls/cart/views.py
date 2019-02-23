from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from takeaway.models import Dish
from .cart import Cart
from .forms import CartAddDishForm


@require_POST
def cart_add(request, dish_id):
    cart = Cart(request)
    dish = get_object_or_404(Dish, id=dish_id)
    form = CartAddDishForm(request.POST)
    if form.is_valid():
        cd = form.changed_data
        cart.add(
            dish=dish,
            quantity=cd['quantity'],
            update_quantity=cd['update']
        )
    return redirect('cart:cart_detail')


def cart_remove(request, dish_id):
    cart = Cart(request)
    dish = get_object_or_404(Dish, id=dish_id)
    cart.remove(dish)
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/detail.html', {'cart': cart})

from decimal import Decimal
from django.conf import settings
from takeaway.models import Dish


class Cart(object):

    def __init__(self, request):
        """
        Initialize the cart
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # We don't have a cart, create a new one
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def __iter__(self):
        """
        Iterate over the items in the cart and
        get the dishes from the database
        """
        dish_ids = self.cart.keys()
        dishes = Dish.objects.filter(id__in=dish_ids)

        cart = self.cart.copy()
        for dish in dishes:
            cart[str(dish.id)]['dish'] = dish

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Count all items in the cart
        """
        return sum(item['quantity'] for item in self.cart.values())

    def add(self, dish, quantity=1, update_quantity=False):
        """
        Add a dish to the cart or update its quantity
        """
        dish_id = str(dish.id)
        if dish_id not in self.cart:
            self.cart[dish_id] = {'quantity': 0,
                                  'price': str(dish.price)}
        if update_quantity:
            self.cart[dish_id]['quantity'] = quantity
        else:
            self.cart[dish_id]['quantity'] += quantity
        self.save()

    def save(self):
        # Mark the session as modified to ensure that it gets saved
        self.session.modified = True

    def remove(self, dish):
        """
        Remove a dish from the cart.
        """
        dish_id = str(dish.id)
        if dish_id in self.cart:
            del self.cart[dish_id]
            self.save()

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()

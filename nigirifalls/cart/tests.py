from django.test import TestCase
from django.urls import reverse
from .cart import Cart
from takeaway.models import Dish
from nigirifalls.settings import CART_SESSION_ID


def create_dish(slug=""):
    """
    Returns a generic dish for testing purposes
    """
    return Dish.objects.create(name="Maki" + slug, image="index.jpg",
                               description="Delicious roll",
                               price=123.00, dish_type="rolls")


class CartTests(TestCase):

    def test_add_dish(self):
        dish = create_dish()
        id = str(dish.id)
        self.client.get('/takeaway/')
        self.client.post(reverse('cart:cart_add', kwargs={'dish_id': id, }),
                         {'quantity': 1, 'update': False})
        cart = self.client.session[CART_SESSION_ID]
        self.assertTrue(cart[id]['quantity'] == 1)

    def test_add_then_remove_dish(self):
        dish = create_dish()
        id = str(dish.id)
        self.client.get('/takeaway/')
        self.client.post(reverse('cart:cart_add', kwargs={'dish_id': id, }),
                         {'quantity': 1, 'update': False})
        cart = self.client.session[CART_SESSION_ID]
        self.assertTrue(cart[id]['quantity'] == 1)
        self.client.post(reverse('cart:cart_remove', kwargs={'dish_id': id, }))
        cart = self.client.session[CART_SESSION_ID]
        with self.assertRaises(KeyError):
            cart[id]

    def test_add_then_update_quantity(self):
        dish = create_dish()
        id = str(dish.id)
        self.client.get('/takeaway/')
        self.client.post(reverse('cart:cart_add', kwargs={'dish_id': id, }),
                         {'quantity': 1, 'update': False})
        cart = self.client.session[CART_SESSION_ID]
        self.assertTrue(cart[id]['quantity'] == 1)
        self.client.post(reverse('cart:cart_add', kwargs={'dish_id': id, }),
                         {'quantity': 2, 'update': True})
        cart = self.client.session[CART_SESSION_ID]
        self.assertTrue(cart[id]['quantity'] == 2)

    def test_add_then_add_n(self):
        dish = create_dish()
        id = str(dish.id)
        self.client.get('/takeaway/')
        self.client.post(reverse('cart:cart_add', kwargs={'dish_id': id, }),
                         {'quantity': 1, 'update': False})
        cart = self.client.session[CART_SESSION_ID]
        self.assertTrue(cart[id]['quantity'] == 1)
        self.client.post(reverse('cart:cart_add', kwargs={'dish_id': id, }),
                         {'quantity': 2, 'update': False})
        cart = self.client.session[CART_SESSION_ID]
        self.assertTrue(cart[id]['quantity'] == 3)

    def test_len(self):
        dish = create_dish()
        id = str(dish.id)
        self.client.get('/takeaway/')
        self.client.post(reverse('cart:cart_add', kwargs={'dish_id': id, }),
                         {'quantity': 1, 'update': False})
        dish = create_dish()
        id = str(dish.id)
        self.client.get('/takeaway/')
        self.client.post(reverse('cart:cart_add', kwargs={'dish_id': id, }),
                         {'quantity': 2, 'update': False})

        cart = Cart(self.client)
        self.assertTrue(len(cart) == 3)

    def test_get_total_price(self):
        dish = create_dish()
        id = str(dish.id)
        self.client.get('/takeaway/')
        self.client.post(reverse('cart:cart_add', kwargs={'dish_id': id, }),
                         {'quantity': 1, 'update': False})
        dish = create_dish()
        id = str(dish.id)
        self.client.get('/takeaway/')
        self.client.post(reverse('cart:cart_add', kwargs={'dish_id': id, }),
                         {'quantity': 2, 'update': False})

        cart = Cart(self.client)
        self.assertTrue(cart.get_total_price() == 3 * dish.price)


class CartDetailViewTests(TestCase):

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/cart/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('cart:cart_detail'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('cart:cart_detail'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cart/detail.html')

    def test_view_contains_desired_data(self):
        response = self.client.get(reverse('cart:cart_detail'))
        number_of_dishes = 5

        for i in range(1, number_of_dishes):
            dish = create_dish(slug=str(i))
            self.client.post(reverse('cart:cart_add',
                             kwargs={'dish_id': dish.id, }),
                             {'quantity': 1, 'update': False})

        response = self.client.get(reverse('cart:cart_detail'))

        for i in range(1, number_of_dishes):
            self.assertContains(response, Dish.objects.get(id=i).name)

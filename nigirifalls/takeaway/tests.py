from django.test import TestCase
from django.urls import reverse
from django.core.validators import ValidationError
from django.utils import timezone

from nigirifalls.settings import CART_SESSION_ID
from .models import Dish, OrderInfo
from .forms import OrderCreateForm


def create_dish(name, description, price, dish_type):
    """
    Create a question with the named parameters.
    """
    return Dish.objects.create(name=name, image="index.jpg",
                               description=description,
                               price=price, dish_type=dish_type)


class DishIndexViewTests(TestCase):

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/takeaway/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('takeaway:index'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('takeaway:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'takeaway/index.html')

    def test_no_dishes(self):
        """
        If no dishes exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('takeaway:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, text='No dishes are availible.')
        self.assertQuerysetEqual(response.context['dish_list'], [])

    def test_has_dish(self):
        """
        If there exists a dish or more, show it to the user.
        """
        create_dish("Maki", "Delicious roll", 123.45, "rolls")
        response = self.client.get(reverse('takeaway:index'))
        self.assertQuerysetEqual(response.context['dish_list'],
                                 ['<Dish: Maki>'])


class OrderInfoFormTests(TestCase):

    def test_invalid_pickup_time(self):
        time = timezone.now() + timezone.timedelta(minutes=29)
        form = OrderCreateForm(data={'name_of_customer': 'Andreas',
                                     'email': "andreas_hh_98@hotmail.no",
                                     'phone_number': 46813998,
                                     'pickup_time': time})
        self.assertFalse(form.is_valid())

    def test_invalid_email(self):
        time = timezone.now() + timezone.timedelta(minutes=31)
        form = OrderCreateForm(data={'name_of_customer': 'Andreas',
                                     'email': "an",
                                     'phone_number': 46813998,
                                     'pickup_time': time})
        self.assertFalse(form.is_valid())

    def test_invalid_phone_number_too_short(self):
        time = timezone.now() + timezone.timedelta(minutes=31)
        form = OrderCreateForm(data={'name_of_customer': 'Andreas',
                                     'email': "andreas_hh_98@hotmail.no",
                                     'phone_number': 112,
                                     'pickup_time': time})
        self.assertFalse(form.is_valid())

    def test_invalid_phone_number_too_long(self):
        time = timezone.now() + timezone.timedelta(minutes=31)
        form = OrderCreateForm(data={'name_of_customer': 'Andreas',
                                     'email': "andreas_hh_98@hotmail.no",
                                     'phone_number': 468139988,
                                     'pickup_time': time})
        self.assertFalse(form.is_valid())

    def test_valid_form(self):
        time = timezone.now() + timezone.timedelta(minutes=31)
        form = OrderCreateForm(data={'name_of_customer': 'Andreas',
                                     'email': "andreas_hh_98@hotmail.no",
                                     'phone_number': 46813998,
                                     'pickup_time': time})
        self.assertTrue(form.is_valid())


class CheckoutViewTests(TestCase):
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/takeaway/checkout/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('takeaway:order_create'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('takeaway:order_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'takeaway/checkout.html')


class ThankYouViewTests(TestCase):

    def setUp(self):
        time = timezone.now() + timezone.timedelta(minutes=31)
        self.order = OrderInfo.objects.create(name_of_customer='Andreas',
                                              email="andreas@hotmail.no",
                                              phone_number=46813998,
                                              pickup_time=time)
        return super().setUp()

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/takeaway/thankyou/' + str(self.order.id))
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('takeaway:thankyou',
                                           args=(self.order.id,)))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('takeaway:thankyou',
                                           args=(self.order.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'takeaway/thankyou.html')


class SearchViewTests(TestCase):

    def setUp(self):
        create_dish("Maki", "Delicious roll", 123.45, "rolls")
        return super().setUp()

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/takeaway/search/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('takeaway:search'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('takeaway:search'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'takeaway/index.html')

    def test_search_by_name(self):
        response = self.client.get('/takeaway/search/?q=maki')
        self.assertContains(response, 'Maki')

    def test_search_by_description(self):
        response = self.client.get('/takeaway/search/?q=Delicious')
        self.assertContains(response, 'Delicious')

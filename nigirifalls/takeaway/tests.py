from django.test import TestCase
from django.urls import reverse
from django.core.validators import ValidationError
from django.utils import timezone
from users.models import CustomUser as User

from nigirifalls.settings import CART_SESSION_ID
from .models import Dish, OrderInfo, Allergen
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

    def test_has_allergens(self):
        """
        If there are allergens in the dish, show it to the user.
        """
        allergen = Allergen.objects.create(name='fish')
        dish = Dish.objects.create(name='Laksemaki', image='index.jpg', description='Klassisk maki', price='123',
                                   dish_type='maki')
        dish.allergy_info.add(allergen)
        response = self.client.get(reverse('takeaway:index'))
        self.assertContains(response, 'F')


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


class UserAccountTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(first_name="Astrid", last_name="Bakken", username='testuser',
                                             password='12345', email="abc@abc.no",
                                             phone_number="88888888")
        self.user.save()
        login = self.client.login(username='testuser', password='12345')
        return super().setUp()

    def test_prepopulated_forms(self):
        """
        If user is logged in, the checkout field should be prepopulated
        """
        # creates user, simulates logged in user
        response = self.client.get(reverse('takeaway:order_create'))
        self.assertContains(response, "Astrid Bakken")
        self.assertContains(response, "88888888")
        self.assertContains(response, "abc@abc.no")

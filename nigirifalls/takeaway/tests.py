from django.test import TestCase
from django.urls import reverse
from django.core.validators import ValidationError

from .models import Dish


def create_dish(name, description, price, dish_type):
    """
    Create a question with the named parameters.
    """
    return Dish.objects.create(name=name, description=description,
                               price=price, dish_type=dish_type)


class DishIndexViewTests(TestCase):
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

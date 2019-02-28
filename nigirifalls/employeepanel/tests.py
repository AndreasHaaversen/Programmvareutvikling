from django.test import TestCase
from django.urls import reverse
from takeaway.models import OrderInfo
from django.utils import timezone

# Create your tests here.


class ActiveOrdersViewTests(TestCase):

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/employeepanel/active_orders/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('employeepanel:active_orders'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('employeepanel:active_orders'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'employeepanel/index.html')

    def test_view_with_active_orders(self):

        time = timezone.now() + timezone.timedelta(minutes=31)
        order = OrderInfo.objects.create(name_of_customer='Test',
                                         email='test@test.no',
                                         phone_number=46813998,
                                         pickup_time=time,
                                         status='prod')
        response = self.client.get(reverse('employeepanel:active_orders'))
        self.assertContains(response, order.name_of_customer)
        self.assertContains(response, order.id)
        self.assertContains(response, str(order.phone_number))
        self.assertContains(response, order.status)

    def test_view_without_active_orders(self):

        time = timezone.now() + timezone.timedelta(minutes=31)
        order = OrderInfo.objects.create(name_of_customer='Test',
                                         email='test@test.no',
                                         phone_number=46813998,
                                         pickup_time=time,
                                         status='cancelled')
        response = self.client.get(reverse('employeepanel:active_orders'))
        self.assertContains(response, 'There are no orders available')

    def test_change_order_status(self):
        time = timezone.now() + timezone.timedelta(minutes=31)
        order = OrderInfo.objects.create(name_of_customer='Test',
                                         email='test@test.no',
                                         phone_number=46813998,
                                         pickup_time=time,
                                         status='accepted')
        id = str(order.id)
        response = self.client.get(reverse('employeepanel:active_orders'))
        self.assertContains(response, order.name_of_customer)
        response = self.client.post(reverse('employeepanel:update_order',
                                            kwargs={'pk': order.id}),
                                    {'status': 'cancelled'})
        self.assertRedirects(response, reverse('employeepanel:active_orders'))
        response = self.client.get(reverse('employeepanel:cancelled_orders'))
        self.assertContains(response, order.name_of_customer)


class CancelledOrdersViewTests(TestCase):

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/employeepanel/cancelled_orders/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('employeepanel:cancelled_orders'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('employeepanel:cancelled_orders'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'employeepanel/index.html')

    def test_view_with_cancelled_orders(self):

        time = timezone.now() + timezone.timedelta(minutes=31)
        order = OrderInfo.objects.create(name_of_customer='Test',
                                         email='test@test.no',
                                         phone_number=46813998,
                                         pickup_time=time,
                                         status='cancelled')
        response = self.client.get(reverse('employeepanel:cancelled_orders'))
        self.assertContains(response, order.name_of_customer)
        self.assertContains(response, order.id)
        self.assertContains(response, str(order.phone_number))
        self.assertContains(response, order.status)

    def test_view_without_cancelled_orders(self):

        time = timezone.now() + timezone.timedelta(minutes=31)
        order = OrderInfo.objects.create(name_of_customer='Test',
                                         email='test@test.no',
                                         phone_number=46813998,
                                         pickup_time=time,
                                         status='prod')
        response = self.client.get(reverse('employeepanel:cancelled_orders'))
        self.assertContains(response, 'There are no orders available')

    def test_change_order_status(self):
        time = timezone.now() + timezone.timedelta(minutes=31)
        order = OrderInfo.objects.create(name_of_customer='Test',
                                         email='test@test.no',
                                         phone_number=46813998,
                                         pickup_time=time,
                                         status='cancelled')
        id = str(order.id)
        response = self.client.get(reverse('employeepanel:cancelled_orders'))
        self.assertContains(response, order.name_of_customer)
        response = self.client.post(reverse('employeepanel:update_order',
                                            kwargs={'pk': order.id}),
                                    {'status': 'prod'})
        self.assertRedirects(response, reverse('employeepanel:active_orders'))
        response = self.client.get(reverse('employeepanel:active_orders'))
        self.assertContains(response, order.name_of_customer)


class CollectedOrdersViewTests(TestCase):

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/employeepanel/collected_orders/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('employeepanel:collected_orders'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('employeepanel:collected_orders'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'employeepanel/index.html')

    def test_view_with_collected_orders(self):
        time = timezone.now() + timezone.timedelta(minutes=31)
        order = OrderInfo.objects.create(name_of_customer='Test',
                                         email='test@test.no',
                                         phone_number=46813998,
                                         pickup_time=time,
                                         status='collected')
        response = self.client.get(reverse('employeepanel:collected_orders'))
        self.assertContains(response, order.name_of_customer)
        self.assertContains(response, order.id)
        self.assertContains(response, str(order.phone_number))
        self.assertContains(response, order.status)

    def test_view_without_cancelled_orders(self):
        time = timezone.now() + timezone.timedelta(minutes=31)
        order = OrderInfo.objects.create(name_of_customer='Test',
                                         email='test@test.no',
                                         phone_number=46813998,
                                         pickup_time=time,
                                         status='prod')
        response = self.client.get(reverse('employeepanel:collected_orders'))
        self.assertContains(response, 'There are no orders available')

    def test_change_order_status(self):
        time = timezone.now() + timezone.timedelta(minutes=31)
        order = OrderInfo.objects.create(name_of_customer='Test',
                                         email='test@test.no',
                                         phone_number=46813998,
                                         pickup_time=time,
                                         status='collected')
        id = str(order.id)
        response = self.client.get(reverse('employeepanel:collected_orders'))
        self.assertContains(response, order.name_of_customer)
        response = self.client.post(reverse('employeepanel:update_order',
                                            kwargs={'pk': order.id}),
                                    {'status': 'cancelled'})
        response = self.assertRedirects(response,
                                        reverse('employeepanel:active_orders'))
        response = self.client.get(reverse('employeepanel:cancelled_orders'))
        self.assertContains(response, order.name_of_customer)


class RedirectViewTests(TestCase):
    def test_redirect(self):
        response = self.client.get('/employeepanel/')
        self.assertRedirects(response, reverse('employeepanel:active_orders'))

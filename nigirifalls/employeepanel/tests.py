from django.test import TestCase
from django.urls import reverse
from django.core import mail
from takeaway.models import OrderInfo, OrderItem, Dish
from django.utils import timezone
from users.models import CustomUser as User


class NotLoggedInViewTests(TestCase):

    def test_active_orders(self):
        response = self.client.get(reverse('employeepanel:active_orders'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'You must be logged in as staff to see this page.')

    def test_cancelled_orders(self):
        response = self.client.get(reverse('employeepanel:cancelled_orders'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'You must be logged in as staff to see this page.')

    def test_collected_orders(self):
        response = self.client.get(reverse('employeepanel:collected_orders'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'You must be logged in as staff to see this page.')


def create_dish(name, description, price, dish_type):
    """
    Create a question with the named parameters.
    """
    return Dish.objects.create(name=name, image="index.jpg",
                               description=description,
                               price=price, dish_type=dish_type)


class ActiveOrdersViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser',
                                             password='12345')
        self.user.is_staff = True
        self.user.save()
        login = self.client.login(username='testuser', password='12345')
        return super().setUp()

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
                                            args=(order.id,)),
                                    {'status': 'cancelled'})
        self.assertRedirects(response, reverse('employeepanel:active_orders'))
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Nigiri Falls - Order no. ' + id)
        response = self.client.get(reverse('employeepanel:cancelled_orders'))
        self.assertContains(response, order.name_of_customer)

    def test_change_order_status_constraint(self):
        time = timezone.now() + timezone.timedelta(minutes=29)
        order = OrderInfo.objects.create(name_of_customer='Test',
                                         email='test@test.no',
                                         phone_number=46813998,
                                         pickup_time=time,
                                         status='accepted')
        id = str(order.id)
        response = self.client.get(reverse('employeepanel:active_orders'))
        self.assertContains(response, order.name_of_customer)
        response = self.client.post(reverse('employeepanel:update_order',
                                            args=(order.id,)),
                                    {'status': 'cancelled'})
        self.assertRedirects(response, reverse('employeepanel:active_orders'))
        response = self.client.get(reverse('employeepanel:cancelled_orders'))
        self.assertNotContains(response, order.name_of_customer)


class CancelledOrdersViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser',
                                             password='12345')
        self.user.is_staff = True
        self.user.save()
        login = self.client.login(username='testuser', password='12345')
        return super().setUp()

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
                                            args=(order.id,)),
                                    {'status': 'prod'})
        self.assertRedirects(response, reverse('employeepanel:active_orders'))
        self.assertEqual(len(mail.outbox), 0)
        response = self.client.get(reverse('employeepanel:active_orders'))
        self.assertContains(response, order.name_of_customer)


class CollectedOrdersViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser',
                                             password='12345')
        self.user.is_staff = True
        self.user.save()
        login = self.client.login(username='testuser', password='12345')
        return super().setUp()

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
                                            args=(order.id,)),
                                    {'status': 'cancelled'})
        response = self.assertRedirects(response,
                                        reverse('employeepanel:active_orders'))
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Nigiri Falls - Order no. ' + id)
        response = self.client.get(reverse('employeepanel:cancelled_orders'))
        self.assertContains(response, order.name_of_customer)

    def test_change_order_status_constraint(self):
        time = timezone.now() + timezone.timedelta(minutes=29)
        order = OrderInfo.objects.create(name_of_customer='Test',
                                         email='test@test.no',
                                         phone_number=46813998,
                                         pickup_time=time,
                                         status='collected')
        id = str(order.id)
        response = self.client.get(reverse('employeepanel:collected_orders'))
        self.assertContains(response, order.name_of_customer)
        response = self.client.post(reverse('employeepanel:update_order',
                                            args=(order.id,)),
                                    {'status': 'cancelled'})
        self.assertRedirects(response, reverse('employeepanel:active_orders'))
        response = self.client.get(reverse('employeepanel:active_orders'))
        self.assertNotContains(response, order.name_of_customer)


class EditOrderViewTests(TestCase):
    def test_view_url_exists_at_desired_location(self):
        time = timezone.now() + timezone.timedelta(minutes=31)
        order = OrderInfo.objects.create(name_of_customer='Test',
                                         email='test@test.no',
                                         phone_number=46813998,
                                         pickup_time=time,
                                         status='collected')
        id = str(order.id)
        response = self.client.get('/employeepanel/order/' + id + '/edit/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        time = timezone.now() + timezone.timedelta(minutes=31)
        order = OrderInfo.objects.create(name_of_customer='Test',
                                         email='test@test.no',
                                         phone_number=46813998,
                                         pickup_time=time,
                                         status='collected')
        response = self.client.get(
            reverse('employeepanel:edit_order', args=(order.id,)))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        time = timezone.now() + timezone.timedelta(minutes=31)
        order = OrderInfo.objects.create(name_of_customer='Test',
                                         email='test@test.no',
                                         phone_number=46813998,
                                         pickup_time=time,
                                         status='collected')
        response = self.client.get(
            reverse('employeepanel:edit_order', args=(order.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'employeepanel/orderedit.html')

#    def test_change_order_info_constraint(self):
#        time = timezone.now() + timezone.timedelta(minutes=29)
#        order = OrderInfo.objects.create(name_of_customer='Test',
#                                         email='test@test.no',
#                                         phone_number=46813998,
#                                         pickup_time=time,
#                                         status='accepted')
#        id = str(order.id)
#        newnumber = 12345678
#        response = self.client.get(
#            reverse('employeepanel:edit_order', args=(order.id,)))
#        self.assertContains(response, order.name_of_customer)
#        response = self.client.post(reverse('employeepanel:edit_order',
#                                            args=(order.id,)),
#                                    {'phone_number': newnumber})
#        response = self.client.get(reverse('employeepanel:active_orders'))
#        self.assertNotContains(response, newnumber)


class EditOrderItemViewTest(TestCase):

    def test_edit_order_item_constraint(self):
        time = timezone.now() + timezone.timedelta(minutes=29)
        makeorder = OrderInfo.objects.create(name_of_customer='Test',
                                             email='test@test.no',
                                             phone_number=46813998,
                                             pickup_time=time,
                                             status='collected')
        makedish = create_dish("Maki", "Delicious roll", 123.45, "rolls")
        orderitem = OrderItem.objects.create(order=makeorder,
                                             dish=makedish,
                                             price=makedish.price,
                                             quantity=1)
        response = self.client.get(
            reverse('employeepanel:edit_order_item', args=(makeorder.id,)))
        response = self.client.post(reverse('employeepanel:edit_order_item',
                                            args=(makeorder.id,)),
                                    {'quantity': 33})
        response = self.client.get(reverse('employeepanel:active_orders'))
        self.assertNotContains(response, 33)

    def test_view_url_exists_at_desired_location(self):
        time = timezone.now() + timezone.timedelta(minutes=31)
        makeorder = OrderInfo.objects.create(name_of_customer='Test',
                                             email='test@test.no',
                                             phone_number=46813998,
                                             pickup_time=time,
                                             status='collected')
        makedish = create_dish("Maki", "Delicious roll", 123.45, "rolls")
        orderitem = OrderItem.objects.create(order=makeorder,
                                             dish=makedish,
                                             price=makedish.price,
                                             quantity=1)
        id = str(orderitem.id)
        response = self.client.get('/employeepanel/order/' + id + '/edititem/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        time = timezone.now() + timezone.timedelta(minutes=31)
        makeorder = OrderInfo.objects.create(name_of_customer='Test',
                                             email='test@test.no',
                                             phone_number=46813998,
                                             pickup_time=time,
                                             status='collected')
        makedish = create_dish("Maki", "Delicious roll", 123.45, "rolls")
        orderitem = OrderItem.objects.create(order=makeorder,
                                             dish=makedish,
                                             price=makedish.price,
                                             quantity=1)
        response = self.client.get(
            reverse('employeepanel:edit_order_item', args=(orderitem.id,)))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        time = timezone.now() + timezone.timedelta(minutes=31)
        makeorder = OrderInfo.objects.create(name_of_customer='Test',
                                             email='test@test.no',
                                             phone_number=46813998,
                                             pickup_time=time,
                                             status='collected')
        makedish = create_dish("Maki", "Delicious roll", 123.45, "rolls")
        orderitem = OrderItem.objects.create(order=makeorder,
                                             dish=makedish,
                                             price=makedish.price,
                                             quantity=1)
        response = self.client.get(
            reverse('employeepanel:edit_order_item', args=(orderitem.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'employeepanel/orderedit.html')


class AddOrderItemViewTests(TestCase):
    def test_view_url_exists_at_desired_location(self):
        time = timezone.now() + timezone.timedelta(minutes=31)
        order = OrderInfo.objects.create(name_of_customer='Test',
                                         email='test@test.no',
                                         phone_number=46813998,
                                         pickup_time=time,
                                         status='collected')
        id = str(order.id)
        response = self.client.get('/employeepanel/order/' + id + '/additem/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        time = timezone.now() + timezone.timedelta(minutes=31)
        order = OrderInfo.objects.create(name_of_customer='Test',
                                         email='test@test.no',
                                         phone_number=46813998,
                                         pickup_time=time,
                                         status='collected')
        response = self.client.get(
            reverse('employeepanel:add_order_item', args=(order.id,)))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        time = timezone.now() + timezone.timedelta(minutes=31)
        order = OrderInfo.objects.create(name_of_customer='Test',
                                         email='test@test.no',
                                         phone_number=46813998,
                                         pickup_time=time,
                                         status='collected')
        response = self.client.get(
            reverse('employeepanel:add_order_item', args=(order.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'employeepanel/orderedit.html')


class RedirectViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser',
                                             password='12345')
        self.user.is_staff = True
        self.user.save()
        login = self.client.login(username='testuser', password='12345')
        return super().setUp()

    def test_redirect(self):
        response = self.client.get('/employeepanel/')
        self.assertRedirects(response, reverse('employeepanel:active_orders'))

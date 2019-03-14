from django.test import TestCase
from .models import CustomUser as User


class TestCustomUserModel(TestCase):

    def test_user_model_to_string(self):
        self.user = User.objects.create_user(username='testuser',
                                             email='me@test.com',
                                             password='12345')
        self.assertEqual(str(self.user), 'me@test.com')

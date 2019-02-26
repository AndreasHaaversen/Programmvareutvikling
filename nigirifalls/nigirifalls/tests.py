from django.test import TestCase
from django.urls import reverse


class TestRedirectView(TestCase):

    def test_redirect_response(self):
        response = self.client.get('')
        self.assertRedirects(response, reverse("takeaway:index"))

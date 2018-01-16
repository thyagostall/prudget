from django.test import TestCase
from django.urls import reverse


class LoginTestCase(TestCase):
    def test_render_login(self):
        response = self.client.get(reverse('login'))

        self.assertContains(response, 'Username')
        self.assertContains(response, 'Password')
        self.assertContains(response, 'Login')

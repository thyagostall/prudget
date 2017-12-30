from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from transactions.testdata import create_user, create_account, create_transaction


class DashboardViewTestCase(TestCase):
    def test_to_index_should_redirect_to_dashboard(self):
        create_user()

        self.client.login(username='username', password='password')

        response = self.client.get('/')

        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse('dashboard')))

    def test_without_user_should_redirect_to_login(self):
        response = self.client.get(reverse('dashboard'))

        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse('login')))

    def test_with_user_should_show_transactions(self):
        create_user()

        logged_successfully = self.client.login(username='username', password='password')
        response = self.client.get(reverse('dashboard'))

        self.assertTrue(logged_successfully)
        self.assertEqual(response.status_code, 200)

    def test_with_user_should_not_shot_others_users_transactions(self):
        first_user = create_user('first', 'first@email.com', 'password')
        second_user = create_user('second', 'second@email.com', 'password')

        first_account = create_account(first_user, 'Itaú', 'BRL')
        second_account = create_account(second_user, 'Itaú', 'BRL')

        first_amount = Decimal('129.99')
        second_amount = Decimal('-75.77')
        create_transaction(first_user, first_account, amount=first_amount)
        create_transaction(second_user, second_account, amount=second_amount)

        logged_successfully = self.client.login(username='first', password='password')

        response = self.client.get(reverse('dashboard'))

        self.assertTrue(logged_successfully)
        self.assertContains(response, '129.99')
        self.assertNotContains(response, '-75.77')

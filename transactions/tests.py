from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from transactions.accounts import transfer_to_account
from transactions.testdata import create_user, create_account, create_transaction


class TransferTestCase(TestCase):
    def test_transfer_transaction(self):
        user = create_user()

        source = create_account(user, 'Itaú', 'BRL')
        destination = create_account(user, 'Carteira', 'BRL')
        transaction = create_transaction(user, source)

        transaction, transfer_transaction = transfer_to_account(transaction, destination)

        self.assertTrue(transaction.group_id.startswith('TRANSF-ACCOUNT-'))
        self.assertTrue(transfer_transaction.group_id.startswith('TRANSF-ACCOUNT-'))
        self.assertEqual(transfer_transaction.group_id, transaction.group_id)

        self.assertEqual(transaction.account, source)
        self.assertEqual(transfer_transaction.account, destination)

        self.assertEqual(transaction.description, transfer_transaction.description)
        self.assertEqual(transaction.date, transfer_transaction.date)
        self.assertEqual(transaction.amount, transfer_transaction.amount)


class AccountTestCase(TestCase):
    def test_get_account_balance(self):
        user = create_user()

        first_amount = Decimal('129.99')
        second_amount = Decimal('-75.77')
        account = create_account(user, 'Itaú', 'BRL')
        create_transaction(user, account, amount=first_amount)
        create_transaction(user, account, amount=second_amount)

        balance = account.balance()

        self.assertEqual(first_amount + second_amount, balance)


class LoginTestCase(TestCase):
    def test_render_login(self):
        response = self.client.get(reverse('login'))

        self.assertContains(response, 'Username:')
        self.assertContains(response, 'Password:')
        self.assertContains(response, 'Login')


class TransactionsViewTestCase(TestCase):
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

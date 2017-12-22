from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from transactions.services import transfer_to_account, transfer_to_user
from transactions.testdata import create_user, create_account, create_transaction, create_bucket


class TransferTestCase(TestCase):
    def test_transfer_between_accounts(self):
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
        self.assertEqual(transaction.amount, -transfer_transaction.amount)

    def test_transfer_between_accounts_of_different_currencies_should_raise(self):
        user = create_user()

        source = create_account(user, 'Cartão Nacional', 'BRL')
        destination = create_account(user, 'International Card', 'USD')
        transaction = create_transaction(user, source)

        with self.assertRaises(ValueError):
            transfer_to_account(transaction, destination)

    def test_transfer_to_another_user_transaction(self):
        source_user = create_user('source.user', 'source@email.com')
        account = create_account(source_user, 'Itaú', 'BRL')

        destination_user = create_user('destination.user', 'destination@email.com')
        create_account(destination_user, 'Inbox Account', 'BRL')

        transaction = create_transaction(source_user, account)

        transaction, expected_transaction = transfer_to_user(transaction, destination_user)

        self.assertEqual(transaction.amount, -expected_transaction.amount)

    def test_transfer_when_not_inbox_account_for_user_should_raise(self):
        source_user = create_user('source.user', 'source@email.com')
        account = create_account(source_user, 'Itaú', 'BRL')
        destination_user = create_user('destination.user', 'destination@email.com')

        transaction = create_transaction(source_user, account)

        with self.assertRaises(Exception):
            transfer_to_user(transaction, destination_user)
            self.fail('Should raise exception')

    def test_transfer_user_when_different_currencies_should_raise(self):
        source_user = create_user('source.user', 'source@email.com')
        account = create_account(source_user, 'Conta Corrente', 'BRL')

        destination_user = create_user('destination.user', 'destination@email.com')
        create_account(destination_user, 'Inbox Account', 'USD')

        transaction = create_transaction(source_user, account)

        with self.assertRaises(ValueError):
            transfer_to_user(transaction, destination_user)
            self.fail('Should raise exception')


class AccountTestCase(TestCase):
    def test_get_account_balance_empty_should_return_zero(self):
        user = create_user()
        account = create_account(user, 'Any account', 'BRL')

        self.assertEqual(Decimal(0), account.balance())

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


class TransactionViewTestCase(TestCase):
    def test_form_is_being_displayed_correctly(self):
        password = 'password'
        user = create_user(password=password)

        self.client.login(username=user.username, password=password)

        response = self.client.get(reverse('new_transaction'))

        self.assertContains(response, 'Description')
        self.assertContains(response, 'Amount')
        self.assertContains(response, 'Date')
        self.assertContains(response, 'Bucket')
        self.assertContains(response, 'Account')
        self.assertContains(response, 'Save')

    def test_form_save_date_correctly(self):
        password = 'password'
        user = create_user(password=password)
        self.client.login(username=user.username, password=password)

        account = create_account(user, name='Account', currency_code='BRL')
        bucket = create_bucket(user, name='Bucket')

        name = 'Some transaction'
        amount = '-90.00'
        date = '02/12/2017'
        data = {
            'description': name,
            'amount': amount,
            'date': date,
            'bucket': bucket.id,
            'account': account.id,
        }

        response_form = self.client.post(reverse('new_transaction'), data)
        response_dasboard = self.client.get(reverse('dashboard'))

        self.assertEqual(response_form.status_code, 302)

        self.assertContains(response_dasboard, name)
        self.assertContains(response_dasboard, amount)
        self.assertContains(response_dasboard, 'Feb. 12, 2017')
        self.assertContains(response_dasboard, bucket.name)
        self.assertContains(response_dasboard, account.name)

    def test_form_can_edit_correctly(self):
        password = 'password'
        user = create_user(password=password)
        self.client.login(username=user.username, password=password)

        account = create_account(user, name='Account', currency_code='BRL')
        bucket = create_bucket(user, name='Bucket')
        transaction = create_transaction(user, account)

        name = 'Another transaction'
        amount = '-90.00'
        date = '02/12/2017'
        data = {
            'description': name,
            'amount': amount,
            'date': date,
            'bucket': bucket.id,
            'account': account.id,
        }

        response_form = self.client.post(reverse('edit_transaction', kwargs={'pk': transaction.id}), pk=transaction.id, data=data)
        response_dasboard = self.client.get(reverse('dashboard'))

        self.assertEqual(response_form.status_code, 302)

        self.assertContains(response_dasboard, name)
        self.assertContains(response_dasboard, amount)
        self.assertContains(response_dasboard, 'Feb. 12, 2017')
        self.assertContains(response_dasboard, bucket.name)
        self.assertContains(response_dasboard, account.name)

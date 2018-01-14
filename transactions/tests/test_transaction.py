import datetime
from decimal import Decimal
from django.test import TestCase
from django.urls import reverse

from transactions.models import Transaction
from transactions.tests.data import create_user, create_account, create_bucket, create_transaction


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

        account = create_account(user, name='Account')
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

        account = create_account(user, name='Account')
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

    def test_debit_transaction_form_only_creates_negative_values(self):
        password = 'password'
        user = create_user(password=password)
        self.client.login(username=user.username, password=password)

        description = 'Debit Transaction'
        amount = '90.00'
        date = '02/12/2017'
        data = {
            'description': description,
            'amount': amount,
            'date': date,
        }

        self.client.post(reverse('new-debit-transaction'), data=data)

        transaction = Transaction.objects.first()
        self.assertEqual(transaction.amount, -Decimal(amount))

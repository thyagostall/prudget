from decimal import Decimal

from django.test import TestCase

from transactions.services import transfer_to_account, get_inbox_account, transfer_to_user
from transactions.testdata import create_user, create_account, create_transaction


class TransferTestCase(TestCase):
    def test_transfer_between_accounts(self):
        user = create_user()

        source = create_account(user, 'Itaú', 'BRL')
        destination = create_account(user, 'Carteira', 'BRL')
        transaction = create_transaction(user, source, amount=Decimal('-10.00'))

        transaction, transfer_transaction = transfer_to_account(transaction, destination)

        self.assertTrue(transaction.group_id.startswith('TRANSF-ACCOUNT-'))
        self.assertTrue(transfer_transaction.group_id.startswith('TRANSF-ACCOUNT-'))
        self.assertEqual(transfer_transaction.group_id, transaction.group_id)

        self.assertEqual(transaction.account, source)
        self.assertEqual(transfer_transaction.account, destination)

        self.assertEqual(transaction.description, transfer_transaction.description)
        self.assertEqual(transaction.date, transfer_transaction.date)
        self.assertEqual(transaction.amount, -transfer_transaction.amount)
        self.assertEqual(transaction.bucket, transfer_transaction.bucket)

    def test_transfer_between_accounts_of_different_currencies_should_raise(self):
        user = create_user()

        source = create_account(user, 'Cartão Nacional', 'BRL')
        destination = create_account(user, 'International Card', 'USD')
        transaction = create_transaction(user, source, amount=Decimal('-10.00'))

        with self.assertRaises(ValueError):
            transfer_to_account(transaction, destination)

    def test_transfer_to_another_user_transaction(self):
        source_user = create_user('source.user', 'source@email.com')
        account = create_account(source_user, 'Itaú', 'BRL')

        destination_user = create_user('destination.user', 'destination@email.com')
        create_account(destination_user, 'Inbox Account', 'BRL')
        destination_account = get_inbox_account(destination_user)

        transaction = create_transaction(source_user, account, amount=Decimal('-10.00'))

        transaction, transfer_transaction = transfer_to_user(transaction, destination_user)

        self.assertTrue(transaction.group_id.startswith('TRANSF-USER-'))
        self.assertTrue(transfer_transaction.group_id.startswith('TRANSF-USER-'))
        self.assertEqual(transfer_transaction.group_id, transaction.group_id)

        self.assertEqual(transfer_transaction.account, destination_account)

        self.assertEqual(transaction.date, transfer_transaction.date)
        self.assertEqual(transaction.amount, -transfer_transaction.amount)

    def test_transfer_when_not_inbox_account_for_user_should_raise(self):
        source_user = create_user('source.user', 'source@email.com')
        account = create_account(source_user, 'Itaú', 'BRL')
        destination_user = create_user('destination.user', 'destination@email.com')

        transaction = create_transaction(source_user, account, amount=Decimal('-10.00'))

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

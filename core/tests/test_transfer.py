from decimal import Decimal

from django.test import TestCase

from core.models.transaction_link import TransactionLink
from core.services import transfer_to_account, get_inbox_account, transfer_to_user, transfer_to_bucket
from core.tests.data import create_user, create_account, create_transaction, create_bucket


class TransferTestCase(TestCase):
    def test_transfer_between_accounts(self):
        user = create_user()
        source_account = create_account(user, 'Source')
        destination_account = create_account(user, 'Destination')
        source_transaction = create_transaction(user, account=source_account, amount=Decimal('-10.00'))

        transaction_link = transfer_to_account(source_transaction, destination_account)
        destination_transaction = transaction_link.destination_transaction

        self.assertEqual(TransactionLink.TRANSFER_ACCOUNT, transaction_link.type)
        self.assertEqual(source_transaction, transaction_link.source_transaction)
        self.assertIsNotNone(transaction_link.destination_transaction)

        self.assertEqual(source_transaction.account, source_account)
        self.assertEqual(destination_transaction.account, destination_account)

        self.assertEqual(source_transaction.description, destination_transaction.description)
        self.assertEqual(source_transaction.date, destination_transaction.date)
        self.assertEqual(source_transaction.amount, -destination_transaction.amount)
        self.assertEqual(source_transaction.bucket, destination_transaction.bucket)

    def test_can_transfer_between_buckets(self):
        user = create_user()
        source_bucket = create_bucket(user, name='Source')
        destination_bucket = create_bucket(user, name='Destination')
        source_transaction = create_transaction(user, bucket=source_bucket, amount=Decimal('-10.00'))

        transaction_link = transfer_to_bucket(source_transaction, destination_bucket)
        destination_transaction = transaction_link.destination_transaction

        self.assertEqual(TransactionLink.TRANSFER_BUCKET, transaction_link.type)
        self.assertEqual(source_transaction, transaction_link.source_transaction)
        self.assertIsNotNone(transaction_link.destination_transaction)

        self.assertEqual(source_transaction.bucket, source_bucket)
        self.assertEqual(destination_transaction.bucket, destination_bucket)

        self.assertEqual(source_transaction.description, destination_transaction.description)
        self.assertEqual(source_transaction.date, destination_transaction.date)
        self.assertEqual(source_transaction.amount, -destination_transaction.amount)
        self.assertEqual(source_transaction.account, destination_transaction.account)

    def test_transfer_to_another_user_transaction(self):
        source_user = create_user('source.user', 'source@email.com')
        source_account = create_account(source_user, 'Source')

        destination_user = create_user('destination.user', 'destination@email.com')
        create_account(destination_user, 'Inbox Account')
        destination_account = get_inbox_account(destination_user)

        source_transaction = create_transaction(source_user, account=source_account, amount=Decimal('-10.00'))

        transaction_link = transfer_to_user(source_transaction, destination_user)
        destination_transaction = transaction_link.destination_transaction

        self.assertEqual(TransactionLink.TRANSFER_USER, transaction_link.type)
        self.assertEqual(source_transaction, transaction_link.source_transaction)
        self.assertIsNotNone(transaction_link.destination_transaction)

        self.assertEqual(destination_transaction.account, destination_account)

        self.assertEqual(source_transaction.description, destination_transaction.description)
        self.assertEqual(source_transaction.date, destination_transaction.date)
        self.assertEqual(source_transaction.amount, -destination_transaction.amount)

    def test_transfer_when_not_inbox_account_for_user_should_raise(self):
        source_user = create_user('source.user', 'source@email.com')
        account = create_account(source_user, 'Itaú')
        destination_user = create_user('destination.user', 'destination@email.com')

        transaction = create_transaction(source_user, account, amount=Decimal('-10.00'))

        with self.assertRaises(Exception):
            transfer_to_user(transaction, destination_user)
            self.fail('Should raise exception')

    def test_transfer_between_accounts_raise_when_source_account_is_empty(self):
        user = create_user()
        source_transaction = create_transaction(user, account=None, amount=Decimal('-10.00'))
        destination_account = create_account(user)

        with self.assertRaises(ValueError):
            transfer_to_account(source_transaction, destination_account)
            self.fail('Should raise exception')

    def test_transfer_between_buckets_raise_when_source_bucket_is_empty(self):
        user = create_user()
        source_transaction = create_transaction(user, bucket=None, amount=Decimal('-10.00'))
        destination_bucket = create_bucket(user)

        with self.assertRaises(ValueError):
            transfer_to_bucket(source_transaction, destination_bucket)
            self.fail('Should raise exception')

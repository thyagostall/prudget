from datetime import datetime
from decimal import Decimal

from django.test import TestCase

from core import services
from core.models.transaction_link import TransactionLink
from core.services.transfer_v2 import TransferException
from core.tests.data import create_bucket, create_user


class TransferTestCase(TestCase):
    def test_transfer_create_two_events_and_event_link(self):
        user = create_user()

        description, date, amount = self.create_description_date_and_amount()
        source_bucket = create_bucket(user, name='Source Bucket')
        destination_bucket = create_bucket(user, name='Destination Bucket')

        transaction_link = self.transfer_bucket(user, description=description, date=date, amount=amount,
                                                source_bucket=source_bucket, destination_bucket=destination_bucket)

        self.assertTransactionEquals(transaction_link.source_transaction, user,
                                     description=description, date=date, amount=amount * -1, bucket=source_bucket)
        self.assertTransactionEquals(transaction_link.destination_transaction, user,
                                     description=description, date=date, amount=amount, bucket=destination_bucket)
        self.assertEqual(transaction_link.type, TransactionLink.TRANSFER_BUCKET)

    def test_transfer_with_same_source_and_destination_bucket_should_raise(self):
        user = create_user()

        description, date, amount = self.create_description_date_and_amount()
        bucket = create_bucket(user, name='Bucket')

        with self.assertRaises(TransferException):
            self.transfer_bucket(user, description=description, date=date, amount=amount,
                                 source_bucket=bucket, destination_bucket=bucket)

    def test_transfer_with_negative_amount_should_raise(self):
        user = create_user()

        description, date, amount = self.create_description_date_and_amount(amount=Decimal('-99.99'))
        source_bucket = create_bucket(user, name='Source Bucket')
        destination_bucket = create_bucket(user, name='Destination Bucket')

        with self.assertRaises(TransferException):
            self.transfer_bucket(user, description=description, date=date, amount=amount,
                                 source_bucket=source_bucket, destination_bucket=destination_bucket)

    @staticmethod
    def create_description_date_and_amount(*, description=None, date=None, amount=None):
        description = description or 'Some description'
        date = date or datetime.today()
        amount = amount or Decimal('120.00')
        return description, date, amount

    @staticmethod
    def transfer_bucket(user, **kwargs):
        return services.transfer_bucket(user, **kwargs)

    def assertTransactionEquals(self, transaction, user, *, description, date, amount, bucket):
        self.assertEqual(transaction.owner, user)
        self.assertEqual(transaction.description, description)
        self.assertEqual(transaction.date, date)
        self.assertEqual(transaction.amount, amount)
        self.assertEqual(transaction.bucket, bucket)
        self.assertIsNone(transaction.account)

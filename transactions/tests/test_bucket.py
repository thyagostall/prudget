import datetime
from decimal import Decimal

from django.test import TestCase

from transactions.tests.data import create_user, create_bucket, create_bucket_value, create_account, \
    create_transaction


class BucketBalanceTestCase(TestCase):
    def test_bucket_balance_with_no_transaction_should_return_bucket_value_amount(self):
        user = create_user()
        bucket = create_bucket(user, 'MyBucket')

        expected_balance = Decimal('400.00')
        create_bucket_value(bucket, amount=expected_balance)

        actual_balance = bucket.balance()

        self.assertEqual(actual_balance, expected_balance)

    def test_bucket_balance_with_transaction_but_no_bucket_value_should_return_transaction_amount_sum(self):
        user = create_user()
        bucket = create_bucket(user, 'MyBucket')
        account = create_account(user, 'Checkings', 'BRL')

        create_transaction(user, account=account, amount=Decimal(-100), bucket=bucket)
        create_transaction(user, account=account, amount=Decimal(-50), bucket=bucket)

        expected_balance = Decimal(-150)
        actual_balance = bucket.balance()

        self.assertEqual(actual_balance, expected_balance)

    def test_bucket_balance_with_transactions_out_of_the_period_should_return_transaction_amount_sum(self):
        user = create_user()
        bucket = create_bucket(user, 'MyBucket')
        account = create_account(user, 'Checkings', 'BRL')

        past_date = datetime.date.today() - datetime.timedelta(days=40)
        create_transaction(user, account=account, amount=Decimal(-100), bucket=bucket, date=past_date)
        create_transaction(user, account=account, amount=Decimal(-50), bucket=bucket)

        expected_balance = Decimal(-50)
        actual_balance = bucket.balance()

        self.assertEqual(actual_balance, expected_balance)

    def test_bucket_balance_with_bucket_value_and_transactions_in_and_out_of_current_period(self):
        user = create_user()
        bucket = create_bucket(user, 'MyBucket')
        account = create_account(user, 'Checkings', 'BRL')

        past_date = datetime.date.today() - datetime.timedelta(days=40)
        create_transaction(user, account=account, amount=Decimal(-100), bucket=bucket, date=past_date)
        create_transaction(user, account=account, amount=Decimal(-50), bucket=bucket)
        create_bucket_value(bucket, amount=Decimal(400))

        expected_balance = Decimal(350)
        actual_balance = bucket.balance()

        self.assertEqual(actual_balance, expected_balance)

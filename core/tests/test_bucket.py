import datetime
from decimal import Decimal

from django.test import TestCase

from core.session_store import set_user_override
from core.tests.data import create_user, create_bucket, create_account, create_transaction


class BucketBalanceTestCase(TestCase):
    def test_bucket_balance_with_no_transaction_should_return_bucket_value_amount(self):
        user = create_user()
        set_user_override(user)

        bucket = create_bucket(user, 'MyBucket')

        expected_balance = Decimal(400.00)
        create_transaction(user, amount=Decimal(400), bucket=bucket)

        actual_balance = bucket.balance()

        self.assertEqual(actual_balance, expected_balance)

    def test_bucket_balance_with_transaction_but_no_bucket_value_should_return_transaction_amount_sum(self):
        user = create_user()
        set_user_override(user)

        bucket = create_bucket(user, 'MyBucket')

        create_transaction(user, amount=Decimal(-100), bucket=bucket)
        create_transaction(user, amount=Decimal(-50), bucket=bucket)

        expected_balance = Decimal(-150)
        actual_balance = bucket.balance()

        self.assertEqual(actual_balance, expected_balance)

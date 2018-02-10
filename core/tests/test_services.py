from decimal import Decimal

from django.test import TestCase

from core import services
from core.tests.data import create_transaction, create_user


class TestServices(TestCase):
    def test_toggle_debit_credit_positive_amount_should_be_changed_to_negative_amount(self):
        transaction = create_transaction(create_user(), amount=Decimal('10.00'))

        services.toggle_credit_debit_and_save(transaction)

        self.assertEqual(Decimal('-10.00'), transaction.amount)

    def test_toggle_debit_credit_negative_amount_should_be_changed_to_positive_amount(self):
        transaction = create_transaction(create_user(), amount=Decimal('-10.00'))

        services.toggle_credit_debit_and_save(transaction)

        self.assertEqual(Decimal('10.00'), transaction.amount)

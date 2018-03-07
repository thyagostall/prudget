from decimal import Decimal

from django.test import TestCase

from core.session_store import set_user_override
from core.tests.data import create_user, create_account, create_transaction


class AccountTestCase(TestCase):
    def test_get_account_balance_empty_should_return_zero(self):
        user = create_user()
        account = create_account(user, 'Any account')

        self.assertEqual(Decimal(0), account.balance())

    def test_get_account_balance(self):
        user = create_user()
        set_user_override(user)

        first_amount = Decimal('129.99')
        second_amount = Decimal('-75.77')
        account = create_account(user, 'Itaú')
        create_transaction(user, account, amount=first_amount)
        create_transaction(user, account, amount=second_amount)

        balance = account.balance()

        self.assertEqual(first_amount + second_amount, balance)

from datetime import datetime
from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase

from transactions.account import transfer_to_account
from transactions.models import Account, Currency, Transaction
from transactions.transaction import create_group_id


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


def create_user():
    return User.objects.create(username='Someone')


def create_account(user, account_name, currency_code):
    currency, _ = Currency.objects.get_or_create(code=currency_code,
                                                 owner=user,
                                                 )
    return Account.objects.create(name=account_name,
                                  currency=currency,
                                  owner=user,
                                  )


def create_transaction(user, source):
    description = 'Some transaction'
    date = datetime.today()
    amount = Decimal('129.99')
    account = source
    group_id = create_group_id()

    return Transaction.objects.create(description=description,
                                      date=date,
                                      amount=amount,
                                      account=account,
                                      group_id=group_id,
                                      owner=user,
                                      )

import pytest

from datetime import datetime

from .dashboard import *
from .account import *
from .transaction import *

def create_fake_account():
    return Account()

def create_fake_credit_transaction(account):
    today = datetime.now()

    transaction_value = 100
    transaction = CreditTransaction(transaction_value, 'Something I received', account, today)

    return transaction

def create_fake_debit_transaction(account):
    today = datetime.now()

    transaction_value = 100
    transaction = DebitTransaction(transaction_value, 'Something I bought', account, today)

    return transaction

def test_create_credit_transaction_dashboard():
    account = create_fake_account()
    transaction = create_fake_credit_transaction(account)
    total_balance = transaction.value

    dashboard = Dashboard()
    dashboard.add_account(account)
    dashboard.add_transaction(transaction)

    return total_balance == dashboard.total_balance

def test_create_debit_transaction_dashboard():
    account = create_fake_account()
    transaction = create_fake_debit_transaction(account)
    total_balance = -transaction.value

    dashboard = Dashboard()
    dashboard.add_account(account)
    dashboard.add_transaction(transaction)

    return total_balance == dashboard.total_balance * -1

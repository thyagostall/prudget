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

    assert total_balance == dashboard.total_balance

def test_create_debit_transaction_dashboard():
    account = create_fake_account()
    transaction = create_fake_debit_transaction(account)
    total_balance = -transaction.value

    dashboard = Dashboard()
    dashboard.add_account(account)
    dashboard.add_transaction(transaction)

    assert total_balance == dashboard.total_balance

def test_get_all_transactions_dashboard():
    account1 = Account()
    account2 = Account()

    transactions = [
            create_fake_credit_transaction(account1),
            create_fake_credit_transaction(account2)
            ]

    dashboard = Dashboard()
    for transaction in transactions:
        dashboard.add_transaction(transaction)

    assert dashboard.transactions == transactions

def test_get_all_accounts_dashboard():
    accounts = [
            Account(),
            Account(),
            Account(),
            Account()
            ]

    dashboard = Dashboard()
    for account in accounts:
        dashboard.add_account(account)

    assert dashboard.accounts == accounts

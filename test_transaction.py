import pytest
from datetime import datetime

from .transaction import * 
from .account import Account

def test_create_a_valid_debit_transaction():
    account = Account()

    today = datetime.now()

    transaction_value = 100
    transaction = DebitTransaction(transaction_value, 'Something I bought', account, today)

    assert account.balance == transaction_value * -1

def test_create_a_valid_credit_transaction():
    account = Account()
    
    today = datetime.now()

    transaction_value = 100
    transaction = CreditTransaction(transaction_value, 'My Salary', account, today)

    assert account.balance == transaction_value

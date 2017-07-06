import pytest

from decimal import Decimal

from .account import Account

def test_decimal_equals_integer():
    assert Decimal('0.5') == 0.5

def test_new_account_balance_is_zero():
    account = Account('Itaú')
    assert account.balance == 0

def test_account_deposit():
    value_deposited = 10
    
    account = Account('Carteira')
    account.deposit(value_deposited)
    assert account.balance == value_deposited
    account.deposit(value_deposited)
    assert account.balance == value_deposited * 2

def test_account_withdraw():
    value_withdrawn = 10
    value_balance = 30

    account = Account('BB')
    account.deposit(value_balance)
    account.withdraw(value_withdrawn)
    assert account.balance == value_balance - value_withdrawn

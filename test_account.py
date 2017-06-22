import pytest

from decimal import Decimal

from .account import Account

def test_decimal_equals_integer():
    assert Decimal('0.5') == 0.5

def test_new_account_balance_is_zero():
    account = Account()
    assert account.balance == 0

def test_account_deposit():
    value_deposited = 10
    account = Account()
    account.deposit(value_deposited)
    assert account.balance == value_deposited

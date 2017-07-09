# -*- coding: utf-8 -*-
import datetime
from decimal import Decimal

from prudget.account import Account
from prudget.commands import *
from prudget.transaction import *


def test_args_to_dictionary():
    result = ['d=2017/01/01', 'v=10.00', 'n="Hello World"']
    keys = ['d', 'n', 'v']
    result = args_to_dictionary(result)
    result = result.keys()

    assert set(keys) == set(result)


def test_create_account_from_command_line_args():
    dictionary = args_to_dictionary(['n=Itaú', 'b=3000.00'])

    parser = Parser()
    result = parser.create_account(dictionary)

    assert result.balance == Decimal(dictionary['b'])
    assert result.name == dictionary['n']


def test_create_debit_transaction_from_command_line_args():
    dictionary = args_to_dictionary(['t=d', 'v=10.00', 'de=Comida', 'da=2017-12-31', 'a=It'])

    itau_account = Account('Itaú')
    accounts = [itau_account]
    date_chosen = datetime.date(2017, 12, 31)

    parser = Parser(accounts)
    result = parser.create_transaction(dictionary)

    assert isinstance(result, DebitTransaction)

    assert result.value == Decimal('10.00')
    assert result.description == 'Comida'
    assert result.account == itau_account
    assert result.date == date_chosen


def test_create_credit_transaction_from_command_line_args():
    dictionary = args_to_dictionary(['t=c', 'v=1000000.01', 'de=Salário', 'da=2017-12-31', 'a=It'])

    itau_account = Account('Itaú')
    accounts = [itau_account]
    date_chosen = datetime.date(2017, 12, 31)

    parser = Parser(accounts)
    result = parser.create_transaction(dictionary)

    assert isinstance(result, CreditTransaction)

    assert result.value == Decimal('1000000.01')
    assert result.description == 'Salário'
    assert result.account == itau_account
    assert result.date == date_chosen
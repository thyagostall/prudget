from decimal import Decimal

import datetime

from prudget.account import Account
from prudget.transaction import CreditTransaction
from prudget.uiprinter.uiaccountprinter import UIAccountPrinter
from prudget.uiprinter.uitransactionprinter import UITransactionPrinter


def create_account_printer():
    return UIAccountPrinter()


def create_transaction_printer():
    return UITransactionPrinter()


def create_account():
    value = Decimal(10)
    account = Account("Itaú")
    account.deposit(value)
    return account


def test_print_account():
    printer = create_account_printer()

    result = printer.print([create_account()])

    expected = ''
    expected += '------------------------------------------\n'
    expected += '|                ACCOUNTS                |\n'
    expected += '------------------------------------------\n'
    expected += '| Itaú                      |      10.00 |\n'
    expected += '------------------------------------------\n'

    assert expected == result


def test_print_transaction():
    value = Decimal(1000)
    transaction = CreditTransaction(value, 'Salário', create_account(), datetime.date(2017, 12, 31))

    printer = create_transaction_printer()
    result = printer.print([transaction])

    expected = ''
    expected += '------------------------------------------------------------------------\n'
    expected += '|                             TRANSACTIONS                             |\n'
    expected += '------------------------------------------------------------------------\n'
    expected += '| C | Salário                   | 2017-12-31 |    1000.00 | Itaú       |\n'
    expected += '------------------------------------------------------------------------\n'

    assert expected == result


def test_print_transaction_details():
    pass

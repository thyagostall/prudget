from decimal import Decimal

from prudget.account import Account
from prudget.uiprinter import UIAccountPrinter


def create_printer():
    return UIAccountPrinter()


def test_print_account():
    value = Decimal(10)
    account = Account("Itaú")
    account.deposit(value)
    printer = create_printer()

    result = printer.print_accounts([account])

    expected = ''
    expected += '------------------------------------------\n'
    expected += '|                ACCOUNTS                |\n'
    expected += '------------------------------------------\n'
    expected += '| Itaú                      |      10.00 |\n'
    expected += '------------------------------------------\n'

    assert expected == result

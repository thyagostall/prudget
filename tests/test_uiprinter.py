from decimal import Decimal

import datetime

from prudget.account import Account
from prudget.envelope import Envelope
from prudget.transaction import CreditTransaction
from prudget.uiprinter.account import UIAccountPrinter
from prudget.uiprinter.envelope import UIEnvelopePrinter
from prudget.uiprinter.transaction import UITransactionPrinter


def create_account_printer(accounts):
    return UIAccountPrinter(accounts)


def create_transaction_printer(transactions):
    return UITransactionPrinter(transactions)


def create_envelope_printer(envelopes):
    return UIEnvelopePrinter(envelopes)


def create_account():
    value = Decimal(10)
    account = Account("Itaú")
    account.deposit(value)
    return account


def test_print_account():
    printer = create_account_printer([create_account()])

    result = printer.print()

    expected = ''
    expected += '------------------------------------------\n'
    expected += '|                ACCOUNTS                |\n'
    expected += '------------------------------------------\n'
    expected += '| Itaú                      |      10.00 |\n'
    expected += '------------------------------------------\n'
    expected += '| Total                     |      10.00 |\n'
    expected += '------------------------------------------\n'

    assert expected == result


def test_print_account_with_no_accounts():
    printer = create_account_printer([])

    result = printer.print()

    expected = 'No Accounts.'

    assert expected == result


def test_print_transaction():
    value = Decimal(1000)
    transaction = CreditTransaction(value, 'Salário', create_account(), datetime.date(2017, 12, 31))

    printer = create_transaction_printer([transaction])
    result = printer.print()

    expected = ''
    expected += '------------------------------------------------------------------------\n'
    expected += '|                             TRANSACTIONS                             |\n'
    expected += '------------------------------------------------------------------------\n'
    expected += '| \033[92mC\033[0m | Salário                   | 2017-12-31 |    1000.00 | Itaú       |\n'
    expected += '------------------------------------------------------------------------\n'

    assert expected == result


def test_print_transaction_with_no_transactions():
    expected = 'No Transactions.'

    printer = create_transaction_printer([])
    result = printer.print()

    assert expected == result


def test_print_envelope_with_no_envelopes():
    expected = 'No Envelopes.'

    printer = create_envelope_printer([])
    result = printer.print()

    assert expected == result


def test_print_envelope_with_envelopes():
    expected = '------------------------------------------\n'
    expected += '|               ENVELOPES                |\n'
    expected += '------------------------------------------\n'
    expected += '| Comida                    |     100.00 |\n'
    expected += '------------------------------------------\n'

    envelope = Envelope('Comida')
    envelope.deposit(100.00)

    printer = create_envelope_printer([envelope])
    result = printer.print()

    assert expected == result

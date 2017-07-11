from decimal import Decimal

import datetime

from prudget.account import Account
from prudget.envelope import Envelope
from prudget.transaction import DebitTransaction


def test_deposit_envelope():
    value = Decimal(10)

    envelope = Envelope('Food')
    envelope.deposit(value)

    assert envelope.balance == value


def test_withdraw_envelope():
    value = Decimal(300)
    pants_price = Decimal(150)

    envelope = Envelope('Clothes')
    envelope.deposit(value)

    account = Account('Checking')
    date = datetime.date(2017, 12, 31)

    DebitTransaction(pants_price, 'Pants', account, date, envelope)

    assert envelope.balance == value - pants_price

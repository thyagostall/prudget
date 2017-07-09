from datetime import datetime
from decimal import Decimal

from prudget.account import Account
from prudget.object_utils import infer_dictionary
from prudget.transaction import *


class InvalidAccountParametersError(Exception):
    pass


class InvalidTransactionTypeError(Exception):
    pass


class InvalidAccountError(Exception):
    pass


class Parser:
    def __init__(self, accounts=None):
        self._accounts = accounts

    def _parse_date(self, dictionary):
        if not 'date' in dictionary:
            date = datetime.today()
            date = date.replace(hour=0, minute=0, second=0, microsecond=0)
            return date
        else:
            date = dictionary['date']
            return datetime.date(datetime.strptime(date, '%Y-%m-%d'))

    def _find_account(self, name):
        for account in self._accounts:
            if account.name.startswith(name):
                return account

        raise InvalidAccountError

    def create_transaction(self, dictionary):
        dictionary = infer_dictionary(dictionary, ['account', 'date', 'name', 'value', 'type'])

        type = self.parse_type(dictionary)
        value = self.parse_value(dictionary)
        description = dictionary['name']
        account = self._find_account(dictionary['account'])
        date = self._parse_date(dictionary)

        if type == 'd':
            return DebitTransaction(value, description, account, date)
        elif type == 'c':
            return CreditTransaction(value, description, account, date)

    def parse_type(self, dictionary):
        if 'type' in dictionary:
            return dictionary['type']
        else:
            return 'd'

    def parse_value(self, dictionary):
        return Decimal(dictionary['value'])

    def create_account(self, dictionary):
        dictionary = infer_dictionary(dictionary, ['name', 'balance'])

        try:
            result = Account(dictionary['name'])
        except KeyError:
            raise InvalidAccountParametersError

        if 'balance' in dictionary:
            result._balance = Decimal(dictionary['balance'])

        return result
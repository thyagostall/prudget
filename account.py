from decimal import Decimal

from .object_utils import infer_dictionary

class Account:
    def __init__(self, name):
        self._balance = Decimal(0)
        self._name = name

    @property
    def balance(self):
        return self._balance

    @property
    def name(self):
        return self._name

    def deposit(self, value):
        self._balance += value

    def withdraw(self, value):
        self._balance -= value

    @staticmethod
    def create_from_dictionary(dictionary):
        keys = ['name', 'balance']
        dictionary = infer_dictionary(dictionary, keys)
        
        result = Account(dictionary['name'])
        result._balance = Decimal(dictionary['balance'])
        return result

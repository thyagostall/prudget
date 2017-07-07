from decimal import Decimal


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
